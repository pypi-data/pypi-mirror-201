# encoding: utf-8
"""
@project: djangoModel->thread_v2
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/7/29 15:11
"""
from django.db.models import F

from xj_user.services.user_detail_info_service import DetailInfoService
from ..models import Thread
from ..models import ThreadExtendData
from ..services.thread_extend_service import ThreadExtendService, ThreadExtendOutPutService
from ..services.thread_statistic_service import StatisticsService
from ..utils.custom_response import util_response
from ..utils.custom_tool import format_params_handle
from ..utils.join_list import JoinList


# 信息服务CURD(支持扩展字段配置)  V2版本
class ThreadItemService:
    @staticmethod
    def add(params):
        # 扩展字段与主表字段拆分
        filter_filed_list = [
            "is_deleted", "category_value", "category_name", "category_id", "classify_id", "classify_value", "classify_name",
            "show_id", "show_value", "show_name", "user_id", "with_user_id",
            "title", "subtitle", "content", "summary", "access_level", "author", "ip", "has_enroll", "has_fee", "has_comment", "has_location",
            "cover", "photos", "video", "files", "price", "is_original", "link",
            "create_time", "update_time", "logs", "more", "sort", "language_code"
        ]
        # 主表 过滤字段
        main_form_data = format_params_handle(
            params.copy(), filter_filed_list=filter_filed_list,
        )
        try:
            instance = Thread.objects.create(**main_form_data)
        except Exception as e:
            return None, f'''{str(e)} in "{str(e.__traceback__.tb_frame.f_globals["__file__"])}" : Line {str(e.__traceback__.tb_lineno)}'''

        # 扩展表 插入或更新
        except_main_form_data = format_params_handle(params.copy(), remove_filed_list=filter_filed_list)
        ThreadExtendService.create_or_update(except_main_form_data, instance.id, main_form_data.get("category_id_id", None))
        return {"id": instance.id}, None

    @staticmethod
    def detail(pk):
        """获取信息内容"""
        thread_dict = Thread.objects.filter(id=pk, is_deleted=False).annotate(
            category_value=F("category__value"),
            category_name=F("category__name"),
            category_platform_code=F("category__platform_code"),
            classify_value=F("classify__value"),
            classify_name=F("classify__name"),
            show_value=F("show__value"),
            show_name=F("show__name"),
        ).values(
            "id", "is_deleted", "category_value", "category_name", "category_id", "classify_id", "classify_value", "classify_name",
            "show_id", "show_value", "show_name", "user_id", "with_user_id",
            "title", "subtitle", "content", "summary", "access_level", "author", "ip", "has_enroll", "has_fee", "has_comment", "has_location",
            "cover", "photos", "video", "files", "price", "is_original", "link",
            "create_time", "update_time", "logs", "more", "sort", "language_code"
        ).first()

        # 信息统计表更新数据
        if not thread_dict:
            return None, "数据不存在"

        # ============ 拼接扩展数据 start ============
        extend_merge_service = ThreadExtendOutPutService(category_id_list=[thread_dict.get("category_id")], thread_id_list=[pk])
        statistic_list = StatisticsService.statistic_list(id_list=[pk])
        user_info_list = DetailInfoService.get_list_detail(user_id_list=[thread_dict["user_id"]] if thread_dict.get("user_id") else [])
        [extend_data_dict] = extend_merge_service.merge([thread_dict])
        [join_statistic_dict] = JoinList(l_list=[extend_data_dict], r_list=statistic_list, l_key="id", r_key='thread_id').join()
        [join_user_info_list] = JoinList(l_list=[join_statistic_dict], r_list=user_info_list, l_key="user_id", r_key='user_id').join()
        # ============ 拼接扩展数据 end  ============
        # 所有访问成功，则进行统计计数
        StatisticsService.increment(thread_id=pk, tag='views', step=1)
        return join_user_info_list, 0

    @staticmethod
    def edit(form_data, pk):
        form_data.setdefault("id", pk)
        # 主表过滤字段
        filter_filed_list = [
            "is_deleted", "category_id", "classify_id", "show", "show_id", "user_id", "with_user_id", "title", "subtitle",
            "content", "summary", "access_level", "author", "ip", "has_enroll", "has_fee", "has_comment", "has_location",
            "cover", "photos", "video", "files", "price", "is_original", "link", "create_time", "update_time", "logs", "more", "sort",
            "language_code"
        ]
        # 主表修改
        main_res = Thread.objects.filter(id=pk)
        if not main_res.first():
            return None, "数据不存在，无法进行修改"
        try:
            # 主表修改
            main_form_data = format_params_handle(form_data.copy(), filter_filed_list=filter_filed_list)
            instance = main_res.update(**main_form_data)
            # 扩展字段修改
            # 排除主表之外的字段，理论上就是扩展字段，接下来仅仅需要转换一下扩展字段
            except_main_form_data = format_params_handle(form_data.copy(), remove_filed_list=filter_filed_list)
            ThreadExtendService.create_or_update(except_main_form_data, pk, main_form_data.get("category_id", None))
            return instance, None
        except Exception as e:
            return None, "信息主表写入异常：" + str(e) + "  line:" + str(e.__traceback__.tb_lineno)

    @staticmethod
    def delete(id):
        main_res = Thread.objects.filter(id=id, is_deleted=0)
        if not main_res:
            return None, "数据不存在，无法进行修改"
        main_res.update(is_deleted=1)
        return None, None

    @staticmethod
    def select_extend(id):
        """单独查询 查询扩展字段"""
        return util_response(list(ThreadExtendData.objects.filter(id=id).values()))
