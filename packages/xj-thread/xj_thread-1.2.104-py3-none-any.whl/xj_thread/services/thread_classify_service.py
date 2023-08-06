# encoding: utf-8
"""
@project: djangoModel->thread_category_item_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 类别单条服务
@created_time: 2022/10/25 14:21
"""
from django.core.paginator import Paginator
from django.db.models import F

from ..models import ThreadClassify
from ..services.thread_category_tree_service import ThreadCategoryTreeServices
from ..utils.custom_tool import format_params_handle, format_list_handle


class ThreadClassifyService():
    @staticmethod
    def edit(edit_params=None, pk=None, search_params=None):
        filtered_edit_params = format_params_handle(
            param_dict=edit_params or {},
            filter_filed_list=["value", "name", "show", "show_id", "description", "category", "category_id", "icon", "sort", "parent_id", "config", ],
        )
        # print("edit_params:", filtered_add_params, "pk:", pk, "search_params:", search_params)
        if not pk and not search_params:
            return None, "没有可编辑的数据"
        # 搜索可修改的数据
        classify_obj = ThreadClassify.objects
        if pk:
            classify_obj = classify_obj.filter(id=pk)
        if search_params:
            classify_obj = classify_obj.filter(**search_params)

        if not classify_obj:
            return None, "没找到可修改的数据"

        instance = classify_obj.update(**filtered_edit_params)
        return instance, None

    @staticmethod
    def delete(pk=None, search_params=None):
        if not pk and not search_params:
            return None, "没有可删除的数据"
        # 搜索可修改的数据
        classify_obj = ThreadClassify.objects
        if pk:
            classify_obj = classify_obj.filter(id=pk)
        if search_params:
            classify_obj = classify_obj.filter(**search_params)

        if not classify_obj:
            return None, "没找到可删除的数据"
        classify_obj.delete()
        return None, None

    @staticmethod
    def add(add_params):
        if not add_params:
            return None, "参数不能为空"

        add_params['parent_id'] = None if not add_params.get("parent_id") else add_params.get("parent_id")
        filtered_add_params = format_params_handle(
            param_dict=add_params,
            filter_filed_list=["id", "value", "name", "show", "show_id", "description", "category", "category_id", "icon", "sort", "parent_id", "config", ],
            is_remove_null=True
        )
        try:
            instance = ThreadClassify.objects.create(**filtered_add_params)
        except Exception as e:
            return None, str(e)
        return instance.to_json(), None

    @staticmethod
    def list(filter_fields_params=None, filter_fields=None, need_pagination=True, need_category_child=None):
        """
        类别。类似于版块大类的概念，用于圈定信息内容所属的主要类别
         """
        # 参数筛选
        if filter_fields_params is None:
            filter_fields_params = {}
        # 分页参数
        page = filter_fields_params.pop("page", 1)
        size = filter_fields_params.pop("size", 10)
        # 是否类别的查询子节点
        if not need_category_child is None:
            category_id = filter_fields_params.pop("category_id", None)
            category_value = filter_fields_params.pop("category_value", None)
            if category_value or category_id:
                filter_fields_params["category_id_list"], err = ThreadCategoryTreeServices.get_child_ids(
                    category_id=category_id,
                    category_value=category_value
                )
        # 搜索参数过滤
        filter_fields_params = format_params_handle(
            param_dict=filter_fields_params,
            filter_filed_list=[
                "id", "value", "name", "sort", 'classify_value',
                "show_id", "show_value", "category_id", "category_id_list", "category_value", "parent_id", "parent_value"
            ],
            alias_dict={"name": "name__contains", "category_id_list": "category_id__in", 'classify_value': "value"}
        )
        # 查询字段筛选
        default_fields = [
            "id", "value", "name", "description", "show_id", "show_value", "category_id", "category_value",
            "icon", "sort", "parent_id", "parent_value", "config"
        ]
        filter_fields_list = format_list_handle(
            param_list=filter_fields.split(";") if filter_fields else [],
            filter_filed_list=default_fields
        )

        classify_set = ThreadClassify.objects.annotate(
            category_value=F('category__value'),
            parent_value=F("parent__value"),
            show_value=F("show__value")
        ).order_by("sort")
        classify_set = classify_set.filter(**filter_fields_params)
        thread_classify_obj = classify_set.values(*filter_fields_list)

        # 不需要分页展示全部数据
        if not need_pagination:
            if not thread_classify_obj:
                return [], None
            return list(thread_classify_obj), None

        # 分页展示
        count = thread_classify_obj.count()
        finish_set = list(Paginator(thread_classify_obj, size).page(page))
        return {'size': int(size), 'page': int(page), 'total': count, 'list': finish_set}, None
