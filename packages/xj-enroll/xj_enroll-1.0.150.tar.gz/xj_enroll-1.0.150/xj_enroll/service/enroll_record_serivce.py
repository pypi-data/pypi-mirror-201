# encoding: utf-8
"""
@project: djangoModel->enroll_record_serivce
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户报名记录
@created_time: 2022/9/17 15:45
"""
from django.core.paginator import Paginator, EmptyPage
from django.db.models import F

from xj_thread.services.thread_list_service import ThreadListService
from xj_user.services.user_detail_info_service import DetailInfoService
from ..models import EnrollRecord, Enroll, EnrollSubitemRecord, EnrollRecordExtendField, EnrollSubitem
from ..serializers import EnrollRecordListSerializer, EnrollRecordListV2Serializer
from ..service.enroll_subitem_record_service import EnrollSubitemRecordService
from ..service.valuation_service import ValuationService
from ..utils.custom_tool import format_params_handle, filter_result_field, write_to_log


class EnrollRecordServices:

    @staticmethod
    def extend_transform_fields(result_list: list = None):
        """
        报名记录列表的扩展字段替换过滤
        :param result_list:
        :return: result_list
        """
        filed_map_list = list(EnrollRecordExtendField.objects.all().values("field", 'field_index'))
        filed_map = {item['field_index']: item['field'] for item in filed_map_list}

        # 扩展字段替换，并过滤
        enroll_record_list = filter_result_field(
            result_list=result_list,
            alias_dict=filed_map
        )
        enroll_record_list = filter_result_field(
            result_list=enroll_record_list,
            remove_filed_list=["field_1", "field_2", "field_3", "field_4", "field_5", "field_6", "field_7", "field_8", "field_9", "field_10"]
        )
        return enroll_record_list

    @staticmethod
    def check_can_add(enroll_id, user_id):
        """
        判断是否可以报名
        :param enroll_id: 报名ID
        :param user_id: 用户ID
        :return: Bool
        """
        if not enroll_id or not user_id:
            return None, "参数错误"

        enrolling_code_start = 23
        enroll_obj = Enroll.objects.filter(id=enroll_id, enroll_status_code__regex=enrolling_code_start).first()
        # 传递的报名ID不正确
        if not enroll_obj:
            return False, "当前报名项不可报名"
        # enroll_json = enroll_obj.to_json()
        enroll_record_obj = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124)  # 拿到搜索报名记录

        # 判断当前的需求分数是否大于等于报名人数 需要改成手动指派可以多人报名，注释下面判断
        # if enroll_json.get("count") <= enroll_record_obj.count():
        #     return False

        # 当前用户报名过了，不允许报名了
        this_user_record_obj = enroll_record_obj.filter(user_id=user_id).first()
        if this_user_record_obj:
            return False, "已经报名，无需再次报名"
        return True, None

    @staticmethod
    def record_add(params):
        """
        报名添加
        :param params: request解析出来的json参数
        :return: 报名记录json
        """
        # 判断是否可以继续报名
        enroll_id = params.get("enroll_id")
        user_id = params.get("user_id")
        if not enroll_id:
            return None, "enroll_id不能为空"

        # 查看是否符合报名条件
        res, err_msg = EnrollRecordServices.check_can_add(enroll_id, user_id)
        if not res:
            return None, err_msg

        filed_map_list = list(EnrollRecordExtendField.objects.all().values("field", 'field_index'))
        reversal_filed_map = {item['field']: item['field_index'] for item in filed_map_list}
        filter_filed_list = list(reversal_filed_map.keys()) + [
            "id", "enroll_id", "user_id", "enroll_auth_status_id", "enroll_pay_status_id", "enroll_status_code", "create_time",
            "price", "deposit", "count", "main_amount", "coupon_amount", "again_reduction", "subitems_amount", "deposit_amount", "amount",
            "paid_amount", "unpaid_amount", "fee", "photos", "files", "score", "reply", "remark", "finish_time",
            "again_price", "again_fee", "initiator_again_price", "estimated_time", "update_time",
        ]

        # 字段过滤
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=filter_filed_list,
            alias_dict=reversal_filed_map
        )
        try:
            # instance, is_create = EnrollRecord.objects.get_or_create(user_id=params["user_id"], enroll_id=params["enroll_id"], defaults=params)
            instance = EnrollRecord.objects.create(**params)
        except Exception as e:
            return None, str(e)
        return instance.to_json(), None

    @staticmethod
    def record_list(params, need_pagination=True):
        try:
            page = int(params.pop('page', 1))
        except Exception as e:
            page = 1
        try:
            size = int(params.pop('size', 10))
        except Exception as e:
            size = 10

        # 根据信息搜索信息ID列表来检索报名记录
        thread_search_prams = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "title", "user_id", "subtitle", "access_level", "author",
                "has_enroll", "has_fee", "has_comment", "has_location", "is_original", "finance_invoicing_code",
                "category_value", "classify_value", "thread_category_value", "thread_classify_value",
                "platform_code", "need_auth", "show_value"
            ],
        )
        if thread_search_prams:
            params["thread_id_list"], err = ThreadListService.search_ids(thread_search_prams, is_strict_mode=False)

        # 扩展字段映射获取
        filed_map_list = list(EnrollRecordExtendField.objects.all().values("field", 'field_index'))
        filed_map = {item['field_index']: item['field'] for item in filed_map_list}
        reversal_filed_map = {item['field']: item['field_index'] for item in filed_map_list}
        filter_filed_list = list(filed_map.values()) + [
            "thread_id_list", "category_id", "id", "enroll_id", "enroll_id_list", "user_id", "enroll_auth_status_id", "enroll_pay_status_id",
            "enroll_status_code", "create_time", "price", "deposit", "count", "main_amount", "coupon_amount", "again_reduction",
            "subitems_amount", "deposit_amount", "amount", "paid_amount", "unpaid_amount", "fee", "photos", "files", "score",
            "reply", "remark", "finish_time", "again_price", "again_fee", "initiator_again_price",
            "estimated_time", "update_time",
        ]

        filter_reversal_filed_map = reversal_filed_map
        filter_reversal_filed_map.update({
            "thread_id_list": "enroll__thread_id__in",
            "enroll_id_list": "enroll_id__in",
            "category_id": "enroll__category_id"
        })
        # 扩展字段筛选
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=filter_filed_list,
            alias_dict=filter_reversal_filed_map
        )
        # PS 124状态码任务取消报名，不予显示
        enroll_obj = EnrollRecord.objects.filter(**params).annotate(
            thread_id=F("enroll__thread_id"),
        ).exclude(enroll_status_code=124)
        count = enroll_obj.count()
        # 是否分页
        if not need_pagination:
            enroll_list = EnrollRecordListSerializer(enroll_obj, many=True).data
        else:
            paginator = Paginator(enroll_obj, size)
            try:
                enroll_obj = paginator.page(page)
            except EmptyPage:
                enroll_obj = paginator.page(paginator.num_pages)

            enroll_list = EnrollRecordListSerializer(enroll_obj, many=True).data
        # 扩展字段替换，并过滤
        enroll_list = filter_result_field(
            result_list=enroll_list,
            alias_dict=filed_map
        )
        enroll_list = filter_result_field(
            result_list=enroll_list,
            remove_filed_list=["field_1", "field_2", "field_3", "field_4", "field_5", "field_6", "field_7", "field_8", "field_9", "field_10"]
        )
        # 拼接用户信息
        user_ids = [i["user_id"] for i in enroll_list]
        user_info_map = {i["user_id"]: i for i in DetailInfoService.get_list_detail(None, user_id_list=user_ids)}
        for j in enroll_list:
            j["user_info"] = user_info_map.get(j["user_id"], {})
        # 返回数据
        return enroll_list if not need_pagination else {'total': count, "page": page, "size": size, 'list': enroll_list}, None

    @staticmethod
    def complex_record_list(params):
        """
        这个接口仅仅提供API使用,不提供服务调用，关联太多的数据，使用了很多的where_in,所以限制分页
        :param params:
        :param need_pagination:
        :return:
        """
        try:
            page = int(params.pop('page', 1))
        except Exception as e:
            page = 1
        try:
            size = int(params.pop('size', 10))
        except Exception as e:
            size = 10

        if size > 100:
            return None, "分布不可以超过100页"
        # 根据信息搜索信息ID列表来检索报名记录
        thread_search_prams = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "title", "user_id", "subtitle", "access_level", "author",
                "has_enroll", "has_fee", "has_comment", "has_location", "is_original", "finance_invoicing_code",
                "category_value", "classify_value", "thread_category_value", "thread_classify_value",
                "platform_code", "need_auth", "show_value"
            ],
        )
        if thread_search_prams:
            # TODO 如果发现查询速度遇到瓶颈，则改成严格模式
            params["thread_id_list"], err = ThreadListService.search_ids(thread_search_prams, is_strict_mode=False)

        # 扩展字段映射获取
        filed_map_list = list(EnrollRecordExtendField.objects.all().values("field", 'field_index'))
        forward_filed_map = {item['field_index']: item['field'] for item in filed_map_list}
        reversal_filed_map = {item['field']: item['field_index'] for item in filed_map_list}
        filter_filed_list = list(forward_filed_map.values()) + [
            "thread_id_list", "id", "category_id", "enroll_id", "user_id", "enroll_auth_status_id", "enroll_pay_status_id", "enroll_status_code", "create_time",
            "price", "deposit", "count", "main_amount", "coupon_amount", "again_reduction", "subitems_amount", "deposit_amount", "amount",
            "paid_amount", "unpaid_amount", "fee", "photos", "files", "score", "reply", "remark", "finish_time",
            "again_price", "again_fee", "initiator_again_price", "estimated_time", "update_time",
        ]
        reversal_filed_map.update({
            "thread_id_list": "enroll__thread_id__in",
            "category_id": "enroll__category_id"
        })

        # 扩展字段筛选
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=filter_filed_list,
            alias_dict=reversal_filed_map
        )
        # PS 124状态码任务取消报名，不予显示
        enroll_obj = EnrollRecord.objects.filter(**params).annotate(
            thread_id=F("enroll__thread_id"),
            enroll_user_id=F("enroll__user_id"),
        ).exclude(enroll_status_code=124)
        count = enroll_obj.count()

        # 是否分页
        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
        except EmptyPage:
            enroll_obj = paginator.page(paginator.num_pages)
        enroll_list = EnrollRecordListV2Serializer(enroll_obj, many=True).data

        # 扩展字段替换，并过滤
        enroll_list = filter_result_field(
            result_list=enroll_list,
            alias_dict=forward_filed_map
        )
        enroll_list = filter_result_field(
            result_list=enroll_list,
            remove_filed_list=["field_1", "field_2", "field_3", "field_4", "field_5", "field_6", "field_7", "field_8", "field_9", "field_10"]
        )

        # 拼接报名用户信息
        user_ids = [i["user_id"] for i in enroll_list]
        user_info_map = {i["user_id"]: i for i in DetailInfoService.get_list_detail(None, user_id_list=user_ids)}
        for j in enroll_list:
            j["enroll_user_info"] = user_info_map.get(j["user_id"], {})

        # 拼接发起人用户信息
        enroll_user_ids = [i["enroll_user_id"] for i in enroll_list]
        user_info_map = {i["user_id"]: i for i in DetailInfoService.get_list_detail(None, user_id_list=enroll_user_ids)}
        for j in enroll_list:
            j["initiator_info"] = user_info_map.get(j["user_id"], {})

        # 拼接信息表
        thread_ids = [i["thread_id"] for i in enroll_list]
        thread_map, err = ThreadListService.search(thread_ids, True)
        for j in enroll_list:
            j["enroll_info"] = thread_map.get(j["thread_id"], {})

        # 返回数据
        return {'total': count, "page": page, "size": size, 'list': enroll_list}, None

    @staticmethod
    def record_edit(params, pk):
        pk = params.pop("id", None) or pk
        # 扩展字段映射获取
        filed_map_list = list(EnrollRecordExtendField.objects.all().values("field", 'field_index'))
        filed_map = {item['field_index']: item['field'] for item in filed_map_list}
        reversal_filed_map = {item['field']: item['field_index'] for item in filed_map_list}
        filter_filed_list = list(filed_map.values()) + [
            "id", "enroll_id", "user_id", "enroll_auth_status_id", "enroll_pay_status_id", "enroll_status_code", "create_time",
            "price", "deposit", "count", "main_amount", "coupon_amount", "again_reduction", "subitems_amount", "deposit_amount", "amount",
            "paid_amount", "unpaid_amount", "fee", "photos", "files", "score", "reply", "remark", "finish_time",
            "again_price", "again_fee", "initiator_again_price", "estimated_time", "update_time",
        ]
        # 扩展字段筛选
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=filter_filed_list,
            alias_dict=reversal_filed_map
        )
        # 数据验证
        record_obj = EnrollRecord.objects.filter(id=pk)
        if not record_obj.first():
            return None, "没有找到id为" + str(pk) + "的记录"
        # 数据进行需改
        try:
            record_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    @staticmethod
    def record_del(pk, search_params=None):
        if pk:
            record_obj = EnrollRecord.objects.filter(id=pk)
        elif search_params and isinstance(search_params, dict):
            record_obj = EnrollRecord.objects.filter(**search_params)
        else:
            return None, "找不到要删除的数据"

        if not record_obj:
            return None, None
        try:
            record_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def record_detail(pk, search_params=None):
        if search_params is None:
            search_params = {}
        # 扩展字段映射获取
        filed_map_list = list(EnrollRecordExtendField.objects.all().values("field", 'field_index'))
        filed_map = {item['field_index']: item['field'] for item in filed_map_list}
        filter_filed_list = list(filed_map.keys()) + [
            # 模型字段
            "id", "enroll_id", "user_id", "enroll_auth_status_id", "enroll_pay_status_id", "enroll_status_code", "create_time",
            "price", "deposit", "count", "main_amount", "coupon_amount", "again_reduction", "subitems_amount", "deposit_amount", "amount",
            "paid_amount", "unpaid_amount", "fee", "photos", "files", "score", "reply", "remark", "finish_time",
            "again_price", "again_fee", "initiator_again_price", "estimated_time", "update_time",
            # 拼接字段
            "subitem_record_list", "user_info"
        ]
        # 搜索数据
        if search_params:
            main_record_detail = EnrollRecord.objects.filter(**search_params).first()
        else:
            main_record_detail = EnrollRecordListSerializer(EnrollRecord.objects.filter(id=pk).first(), many=False).data
        # 拼接报名分项记录
        main_record_detail["subitem_record_list"], err = EnrollSubitemRecordService.list({"enroll_record_id": pk}, False)
        # 拼接用户信息
        main_record_detail["user_info"], err = DetailInfoService.get_detail(user_id=main_record_detail["user_id"])
        # 扩展字段过滤
        main_record_detail = format_params_handle(
            param_dict=main_record_detail,
            filter_filed_list=filter_filed_list,
            alias_dict=filed_map
        )
        main_record_detail = format_params_handle(
            param_dict=main_record_detail,
            remove_filed_list=["field_1", "field_2", "field_3", "field_4", "field_5", "field_6", "field_7", "field_8", "field_9", "field_10"]
        )
        return main_record_detail, None

    @staticmethod
    def appoint(enroll_id, record_id, subitem_id):
        """
        镖行天下，报名人指派。
        :param enroll_id: 报名ID
        :param record_id: 记录ID
        :param subitem_id: 分项ID
        :return: None，err_msg
        """
        # 定义常量
        draft_code = 124
        draft_start = "^1"
        enrolled_code = 356
        enrolled_start = "^3"
        enrolling_code = 234

        try:
            # 获取报名主体，确认传的enroll_id是否存在
            enroll_query_set = Enroll.objects.filter(id=enroll_id, enroll_status_code__regex=enrolling_code).first()
            if not enroll_query_set:
                return None, "没有找到可以报名的报名主体"

            # 报名记录检查是否存在
            this_record_obj = EnrollRecord.objects.filter(id=record_id).exclude(enroll_status_code=draft_code).first()
            if not this_record_obj:
                return None, "找不到该报名人记录"

            # 校验报名分项是否存在
            enroll_subitem_obj = EnrollSubitem.objects.filter(id=subitem_id).first()
            if not enroll_subitem_obj:
                return None, "subitem_id错误，找不到可以指派的任务"

            # 判断当前的任务是否已经被指派过
            enroll_subitem_record_obj = EnrollSubitemRecord.objects.filter(enroll_subitem_id=subitem_id) \
                .exclude(enroll_subitem_status_code__regex=draft_start).first()
            if not enroll_subitem_record_obj is None:
                return None, "该任务已经指派过了，无法在指派给其他人。"

            # 判断是否剩余可指派的任务
            need_count = enroll_query_set.count or 0  # 需求份数
            enrolled_count = EnrollSubitemRecord.objects.annotate(enroll_id=F("enroll_record__enroll_id")) \
                .filter(enroll_id=enroll_id).exclude(enroll_subitem_status_code__regex=draft_start).values("id").count()
            if enrolled_count >= int(need_count):  # 报名成功的数量
                return None, "已经没有剩余的任务了，无法再次指派"

            # 指派某个人做哪一个任，生成任务记录（生成一条报名分项记录）
            insert_params = {
                "enroll_record_id": record_id,
                "enroll_subitem_id": subitem_id,
                "user_id": this_record_obj.user_id,
                "enroll_subitem_status_code": enrolled_code,
                "price": enroll_subitem_obj.price,
                "count": enroll_subitem_obj.count,
                "subitem_amount": enroll_subitem_obj.price
            }
            EnrollSubitemRecord.objects.create(**insert_params)

            # 判断是否多个任务指派给一个人，修改报名记录得到count, count表示这个报名人拥有几个任务（分项记录） 修改当前的报名记录未被指派状态，变成已经指派
            subitem_record_count = EnrollSubitemRecord.objects.filter(enroll_record_id=record_id).count()
            subitems_amount = (this_record_obj.price or 0 + this_record_obj.again_price or 0) * subitem_record_count

            EnrollRecord.objects.filter(id=record_id).update(enroll_status_code=enrolled_code, count=subitem_record_count, amount=subitems_amount)
            EnrollSubitem.objects.filter(enroll_id=enroll_id).update(enroll_subitem_status_code=enrolled_code)

            # 再次查询 报名成功的数量, 判断是否可以进入补差补差价。
            # 查询当前指派的人数，和需求的数量，如果相同则指派满，<报名中> ==>> <已报名>
            again_enrolled_count = EnrollSubitemRecord.objects.annotate(enroll_id=F("enroll_record__enroll_id")) \
                .filter(enroll_id=enroll_id, enroll_subitem_status_code__regex=enrolled_start).values("id").count()
            if again_enrolled_count >= need_count:
                # 如果是一人被指派多份的时候就会出现问题，所以应该使用左连接，以报名分项记录为主表连接报名记录表，enroll_id为搜索
                valuate_result, err = ValuationService.valuation_detailed_list(enroll_id)
                if err:
                    write_to_log(prefix="报名指派重新计价异常：", content=err)

                # 报名主表更新
                Enroll.objects.filter(id=enroll_id).update(
                    enroll_status_code=enrolled_code,
                    unpaid_amount=valuate_result["unpaid_amount"],
                    amount=valuate_result["amount"],
                    commision=valuate_result["commision"],
                    subitems_amount=valuate_result["subitems_amount"],
                )

                # 把剩余没有指派的人全部变成草稿状态
                EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code__regex=enrolled_start).update(enroll_status_code=draft_code)
            return None, None

        except Exception as e:
            write_to_log(level="error", prefix="报名指派异常", err_obj=e)
            return None, str(e)
