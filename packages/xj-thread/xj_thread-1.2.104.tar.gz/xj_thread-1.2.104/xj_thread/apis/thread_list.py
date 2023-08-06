"""
Created on 2022-04-11
@description:刘飞
@description:发布子模块逻辑分发
"""
import datetime

from rest_framework.views import APIView

from xj_user.services.user_detail_info_service import DetailInfoService
from ..services.thread_category_tree_service import ThreadCategoryTreeServices
from ..services.thread_list_service import ThreadListService
from ..services.thread_statistic_service import StatisticsService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, filter_result_field, filter_fields_handler
from ..utils.join_list import JoinList
from ..utils.user_wrapper import user_authentication_wrapper


class ThreadListAPIView(APIView):
    """
    get: 信息表列表
    post: 信息表新增
    """

    # 我们更希望通过装饰器来做权限验证，这样可以更好的精简API层的代码量 2022.10.3 by Sieyoo
    @user_authentication_wrapper  # 如果有token则返回user_info，无则返回空
    @request_params_wrapper
    def get(self, *args, user_info=None, request_params, **kwargs):
        request_params.setdefault("category_value", kwargs.get("category_value", None))

        # 是否检查子树的的信息,如果category_id或者category_value都没传则查询全部
        need_child = request_params.pop('need_child', None)
        if need_child:
            if not request_params.get("category_id") and not request_params.get("category_value"):
                return util_response(msg="您选择了need_child，无法搜索到对应节点")

            category_ids, category_tree_err = ThreadCategoryTreeServices.get_child_ids(
                category_id=request_params.pop("category_id", None),
                category_value=request_params.pop("category_value", None)
            )
            if category_tree_err:
                return util_response(err=1000, msg="获取字数节点错误：" + category_tree_err)
            request_params.setdefault("category_id_list", category_ids)

        # 检查时间格式
        try:
            if request_params.get('create_time_start'):
                datetime.datetime.strptime(request_params.get('create_time_start'), "%Y-%m-%d %H:%M:%S")
            if request_params.get('create_time_end'):
                datetime.datetime.strptime(request_params.get('create_time_end'), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return util_response(err=1001, msg="时间格式错误:它的格式应该是YYYY-MM-DD HH:MM:SS")

        # 获取列表数据
        thread_serv, error_text = ThreadListService.list(request_params)
        if error_text:
            return util_response(err=1002, msg=error_text)

        # 按权限自动过滤数据
        thread_id_list = list(set([item['id'] for item in thread_serv['list'] if item['id']]))
        user_id_list = list(set([item['user_id'] for item in thread_serv['list'] if item['user_id']]))

        # 用户数据和统计数据 合并
        statistic_list = StatisticsService.statistic_list(id_list=thread_id_list)
        user_info_list = DetailInfoService.get_list_detail(user_id_list=user_id_list)
        thread_serv['list'] = JoinList(l_list=thread_serv['list'], r_list=statistic_list, l_key="id", r_key='thread_id').join()
        thread_serv['list'] = JoinList(l_list=thread_serv['list'], r_list=user_info_list, l_key="user_id", r_key='user_id').join()

        # 过滤字段
        default_fields = [
            "id", "category_name", "classify_name", "show_value", "title", "subtitle", "summary",
            "cover", "photos", "video", "author", "avatar", "user_name", "nickname",
            "weight", "views", "plays", "comments", "likes", "favorite", "shares", "create_time", "update_time"
        ]
        filter_fields = filter_fields_handler(
            default_field_list=default_fields,
            input_field_expression=request_params.pop('filter_fields', None)
        )
        thread_serv['list'] = filter_result_field(
            result_list=thread_serv['list'],
            filter_filed_list=filter_fields
        )

        return util_response(data=thread_serv, is_need_parse_json=True)
