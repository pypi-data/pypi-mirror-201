# _*_coding:utf-8_*_

from rest_framework.views import APIView

from xj_user.utils.user_wrapper import user_authentication_force_wrapper
from ..services.flow_process_service import FlowProcessService
from ..utils.custom_response import util_response
from ..utils.request_params_wrapper import request_params_wrapper


class FlowProcess(APIView):

    def __init__(self, *args, **kwargs):
        self.flow_process_service = FlowProcessService()
        super().__init__(*args, **kwargs)

    @request_params_wrapper
    @user_authentication_force_wrapper
    def post(self, request, request_params=None, *args, user_info=None, **kwargs):
        """
        流程作业
        """
        flow_node_id = request_params.pop('flow_node_id', None)
        flow_action_id = request_params.pop('flow_action_id', None)
        if not flow_node_id:
            return util_response(err=1001, msg='flow_node_id 必填')
        if not flow_action_id:
            return util_response(err=1001, msg='flow_action_id 必填')
        data, error_text = self.flow_process_service.do_once_flow(
            flow_node_id=flow_node_id,
            flow_action_id=flow_action_id,
            source_params=request_params,
            user_info=user_info
        )
        if error_text:
            return util_response(err=error_text)
        return util_response(data=data)
