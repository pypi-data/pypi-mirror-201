from django.contrib import admin

from .models import Flow, FlowNode, FlowAction, FlowNodeToAction, FlowActionToOperator, FlowNodeActionRule, FlowNodeLog, FlowRecord, FlowLastStatus


class FlowAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow_name', 'module_name', 'description')
    fields = ('id', 'flow_name', 'module_name', 'description')
    search_fields = ('id', 'flow_name', 'module_name')
    readonly_fields = ['id']
    list_per_page = 20


class FlowToCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow', 'category_id',)
    fields = ('id', 'flow', 'category_id',)
    search_fields = ('id', 'flow', 'category_id',)
    readonly_fields = ['id']
    list_per_page = 20


class FlowNodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow_id', 'node_name', 'node_value', 'module_name', 'flow_number', 'status_code', 'summary', 'description')
    fields = ('id', 'flow_id', 'node_name', 'module_name', 'node_value', 'flow_number', 'status_code', 'summary', 'description')
    search_fields = ('id', 'flow_id', 'node_name', 'module_name', 'summary')
    readonly_fields = ['id']
    ordering = ['flow_id', "flow_number"]
    list_per_page = 20


class FlowActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'name', 'description', 'config')
    fields = ('id', 'action', 'name', 'description', 'config')
    search_fields = ('id', 'action', 'name', 'description', 'config')
    readonly_fields = ['id']
    ordering = ['action']
    list_per_page = 20


class FlowNodeToActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow_id', 'flow_node_id', 'flow_action_id', 'flow_to_node_id', "flow_to_fail_node_id", "ttl", 'role_list', 'user_list', "is_automatic", "description")
    fields = ('id', 'flow_id', 'flow_node_id', 'flow_action_id', 'flow_to_node_id', "flow_to_fail_node_id", "ttl", 'role_list', 'user_list', "is_automatic", "description")
    search_fields = ('id', 'flow_node_id', 'flow_action_id', 'flow_to_node_id')
    readonly_fields = ['id', 'flow_id']
    ordering = ['flow_node_id__flow_id', 'flow_node_id__flow_number', 'flow_to_node_id']
    list_filter = ['flow_node_id__flow_id']

    def flow_id(self, item):
        return item.flow_node_id.flow_id


    flow_id.short_description = '流程ID'
    list_per_page = 20


class FlowActionToOperatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow_action_id', 'role_id', 'user_id')
    fields = ('id', 'flow_action_id', 'role_id', 'user_id')
    search_fields = ('id', 'flow_action_id', 'role_id', 'user_id')
    readonly_fields = ['id']
    list_per_page = 20


class FlowNodeActionRuleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'flow_node_to_action_id', 'rule_name', 'rule_sort', 'inflow_service', 'inflow_module', 'inflow_field', 'outflow_module', 'outflow_field', 'default_value', 'expression_string',
        'python_script')
    fields = ('id', 'flow_node_to_action_id', 'rule_name', 'rule_sort', 'inflow_service', 'inflow_module', 'inflow_field', 'outflow_module', 'outflow_field', 'default_value', 'expression_string',
              'python_script')
    search_fields = ('id', 'rule_name', 'inflow_service', 'inflow_module', 'inflow_field', 'outflow_field')
    readonly_fields = ['id']
    ordering = ['flow_node_to_action_id__flow_node_id__flow_id', 'flow_node_to_action_id__flow_node_id__flow_number', 'rule_sort']
    list_per_page = 20


class FlowRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow_node_id', 'user_id', 'belong_role_id', 'summary')
    fields = ('id', 'flow_node_id', 'user_id', 'belong_role_id', 'summary')
    search_fields = ('id', 'flow_node_id', 'user_id', 'belong_roid_id', 'summary')
    readonly_fields = ['id']
    list_per_page = 20


class FlowNodeLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow_record_id', 'flow_node_id', 'user_id', 'belong_role_id', 'summary', 'create_time')
    fields = ('id', 'flow_record_id', 'flow_node_id', 'user_id', 'belong_role_id', 'summary', 'create_time')
    search_fields = ('id', 'flow_record_id', 'flow_node_id', 'user_id', 'summary')
    readonly_fields = ['id', 'create_time']
    list_per_page = 20


class FlowLastStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "module_code", "table_code", "relate_data_id", "flow_node_id", "user_id")
    fields = ("id", "module_code", "table_code", "relate_data_id", "flow_node_id", "user_id")
    search_fields = ("id", "module_code", "table_code", "relate_data_id", "flow_node_id", "user_id")
    readonly_fields = ['id', ]
    list_per_page = 20


admin.site.register(Flow, FlowAdmin)
admin.site.register(FlowNode, FlowNodeAdmin)
admin.site.register(FlowAction, FlowActionAdmin)
admin.site.register(FlowNodeToAction, FlowNodeToActionAdmin)
admin.site.register(FlowActionToOperator, FlowActionToOperatorAdmin)
admin.site.register(FlowNodeActionRule, FlowNodeActionRuleAdmin)
admin.site.register(FlowRecord, FlowRecordAdmin)
admin.site.register(FlowNodeLog, FlowNodeLogAdmin)
admin.site.register(FlowLastStatus, FlowLastStatusAdmin)
