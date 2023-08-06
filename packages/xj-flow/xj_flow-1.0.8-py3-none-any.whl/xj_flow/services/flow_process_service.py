# _*_coding:utf-8_*_

from django.db import transaction
from django.db.models import F

from ..models import FlowNodeActionRule
from ..utils.custom_tool import *
from ..utils.j_valuation import JExpression


class FlowProcessService:
    def __do_by_default_value(self, source_params, rule):
        """通过默认值进行赋值"""
        if not rule.get("outflow_field", None):
            return source_params
        try:
            rule["default_value"] = json.loads(rule["default_value"])
        except Exception as e:
            pass

        source_params.setdefault(rule["outflow_field"], rule["default_value"])
        return source_params

    def __do_by_expression(self, source_params, rule):
        """通过表达式进行赋值"""
        if not rule.get("outflow_field", None):
            return source_params

        if rule.get("expression_string", None):
            # 公式字符串，变量解析替换
            expression_string, parsed_variable_map = JExpression.parse_variables(
                rule["expression_string"],
                source_params
            )
            # 实例化计算器类，并且计算结果
            calculator = JExpression()
            data, err = calculator.process(expression_string)
            # 结果赋值
            data = round(data, 2) if isinstance(data, float) else data
            source_params[rule["outflow_field"]] = data

        return source_params

    def __do_by_python_script(self, source_params, rule):
        """执行脚本方法"""
        if not rule.get("outflow_field", None):
            return source_params

        if rule.get("python_script", None):
            # 创建栈空间，并传入流入流程的字段和值
            inflow_field = rule["outflow_field"]
            params = {inflow_field: source_params[inflow_field]}
            # TODO 这个python_script 最好做成密文存取
            exec(rule["python_script"], params)
            inflow_filed_result = params.get(inflow_field, None)
            # 处理后的结果赋值
            source_params[inflow_field] = inflow_filed_result if inflow_filed_result else source_params[inflow_field]
        return source_params

    def do_once_flow(self, flow_node_id, flow_action_id, source_params=None, user_info=None):
        """
        根据流程节点调用配置好的服务方法，也可以执行表达式，脚本，默认字
        @param flow_node_id 流程节点ID
        @param flow_action_id 希望处理的流程动作ID
        @param source_params 需要处理的原数据
        :return flow_id, msg
        """
        if source_params is None:
            source_params = {}

        if not user_info:
            return None, "权限错误，请重新登录"

        flow_rule_list = list(
            FlowNodeActionRule.objects.annotate(next_node_id=F("flow_node_to_action_id__flow_to_node_id")).filter(
                flow_node_to_action_id__flow_node_id=flow_node_id,
                flow_node_to_action_id__flow_action_id=flow_action_id,
            ).values()
        )

        if not flow_rule_list:
            return None, "没有找到流程规则"

        process_context = []  # 流程处理上下文
        next_node_id = flow_rule_list[0]["next_node_id"]  # 进入的下一个流程节点
        # 开始事务
        sid = transaction.savepoint()
        original_params = source_params.copy()  # 注意这里出现引用赋值的问题，指针没有分裂，所以使用方法强制分类赋值一份
        # print("original_params:", original_params, "flow_rule_list:", flow_rule_list, "next_node_id:", next_node_id)
        # 执行所有的方法
        for item in flow_rule_list:
            current_context = {}
            current_context["original_params"] = original_params
            # 参数初始化
            source_params = self.__do_by_default_value(source_params, item)
            source_params = self.__do_by_expression(source_params, item)
            source_params = self.__do_by_python_script(source_params, item)
            current_context["inited_params"] = source_params
            # 没有配置模块和服务
            if not item.get("inflow_module", None) or not item.get("inflow_service", None):
                process_context.append(current_context)
                continue

            # 配置了模块，但是没有对外开放，直接返回预处理的数据
            model = sys.modules.get(item["inflow_module"], None)
            if not model:
                process_context.append(current_context)
                current_context["result"] = current_context["err_msg"] = None
                continue

            # 加载需要的服务，如果没有可执行的服务方法，返回预处理的数据
            service = getattr(model, item["inflow_service"], None)
            if service:
                try:
                    input_params = service_params_adapter(service, source_params)
                    data, err = service(**input_params)
                    current_context["result"] = data
                    current_context["err_msg"] = err
                    process_context.append(current_context)
                    if err:
                        # 执行错误，则进行回滚，返回执行记录
                        transaction.savepoint_rollback(sid)
                        break
                except Exception as e:
                    transaction.savepoint_rollback(sid)
                    current_context["result"] = None
                    current_context["err_msg"] = "停止运行，原因如下：" + str(e)
                    process_context.append(current_context)
                    break
            else:
                current_context["result"] = current_context["err_msg"] = None

        # 完成执行，清除所有的点
        transaction.clean_savepoints()
        # ================================================================================#
        # TODO 记录用户流程的最后状态,待完成。如果流程通过交互控制，就是无状态。流程就是辅助。
        # user_id = user_info.get("user_id")
        # FlowLastStatus.objects.filter(user_id=user_id, flow_node_id=flow_node_id)
        # ================================================================================#
        return {"process_context": process_context, "next_node_id": next_node_id}, None

    def do_once_flow_in_service(self, flow_node_id=None, flow_action_id=None, flow_node_value=None, flow_action_value=None, source_params: dict = None):
        """
        根据流程节点调用配置好的服务方法，也可以执行表达式，脚本，默认字
        @param flow_node_id 流程节点ID
        @param flow_action_id 希望处理的流程动作ID
        @param source_params 需要处理的原数据
        :param flow_action_value: 动作Value
        :param flow_node_value:
        :return flow_id, msg
        """
        if source_params is None:
            source_params = {}

        err_msg = None  # 监听全流程服务执行的错误异常信息

        if (not flow_node_id and not flow_node_value) or (not flow_action_id and not flow_action_value):
            return {"source_params": source_params}, None

        search_params = format_params_handle(
            param_dict={
                "flow_node_to_action_id__flow_node_id": flow_node_id,
                "flow_node_to_action_id__flow_action_id": flow_action_id,
                "flow_node_to_action_id__flow_node_id__node_value": flow_node_value,
                "flow_node_to_action_id__flow_action_id__action": flow_action_value,
            },
            remove_filed_list=[""],
            is_remove_empty=True,
        )
        flow_rule_list = list(
            FlowNodeActionRule.objects.annotate(next_node_id=F("flow_node_to_action_id__flow_to_node_id")).filter(**search_params).values()
        )
        if not flow_rule_list:
            return {"source_params": source_params}, "flow_node_id或者flow_action_id错误,没有找到可执行流程"

        process_context = []  # 流程处理上下文
        next_node_id = flow_rule_list[0]["next_node_id"]  # 进入的下一个流程节点
        sid = transaction.savepoint()  # 开始事务
        original_params = source_params.copy()  # 注意这里出现引用赋值的问题，指针没有分裂，所以使用方法强制分类赋值一份
        # print("original_params:", original_params, "flow_rule_list:", flow_rule_list, "next_node_id:", next_node_id)
        # 执行所有的方法
        for item in flow_rule_list:
            current_context = {}
            current_context["source_params"] = original_params
            # 参数初始化
            source_params = self.__do_by_default_value(source_params, item)
            source_params = self.__do_by_expression(source_params, item)
            source_params = self.__do_by_python_script(source_params, item)
            current_context["inited_params"] = source_params
            # 没有配置模块和服务
            if not item.get("inflow_module", None) or not item.get("inflow_service", None):
                process_context.append(current_context)
                continue

            # 配置了模块，但是没有对外开放，直接返回预处理的数据
            model = sys.modules.get(item["inflow_module"], None)

            if not model:
                process_context.append(current_context)
                current_context["result"] = current_context["err_msg"] = None
                continue

            # 加载需要的服务，如果没有可执行的服务方法，返回预处理的数据
            service = getattr(model, item["inflow_service"], None)
            if service:
                try:
                    input_params = service_params_adapter(service, source_params)
                    data, err = service(**input_params)
                    current_context["result"] = data
                    current_context["err_msg"] = err
                    process_context.append(current_context)
                    if err:
                        # 执行错误，则进行回滚，返回执行记录
                        err_msg = err
                        transaction.savepoint_rollback(sid)
                        break
                except Exception as e:
                    # print(e)
                    # print(e.__traceback__.tb_frame.f_globals["__file__"])
                    # print(e.__traceback__.tb_lineno)
                    transaction.savepoint_rollback(sid)
                    current_context["result"] = None
                    current_context["err_msg"] = err_msg = "停止运行，原因如下：" + str(e)
                    process_context.append(current_context)
                    break
            else:
                current_context["result"] = current_context["err_msg"] = None

        # 完成执行，清除所有的点
        transaction.clean_savepoints()
        return {"source_params": source_params, "process_context": process_context, "next_node_id": next_node_id}, err_msg
