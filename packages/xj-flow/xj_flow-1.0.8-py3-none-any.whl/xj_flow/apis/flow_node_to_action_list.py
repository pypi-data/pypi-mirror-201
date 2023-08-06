# _*_coding:utf-8_*_

from rest_framework.views import APIView
from ..services.flow_process_service import FlowProcessService
from ..services.flow_basic_service import FlowBasicService
from ..utils.custom_response import util_response
from ..utils.request_params_wrapper import request_params_wrapper


class FlowNodeToActionList(APIView):
    @request_params_wrapper
    def get(self, request, request_params=None):
        """
        流程作业
        """
        # print("FlowNodeToActionList: request_params:", request_params)
        flow_id = request_params.get('flow_id', None)
        flow_list, error_text = FlowBasicService.get_flow_node_to_action_list(flow_id=flow_id)

        return util_response(data=flow_list)
