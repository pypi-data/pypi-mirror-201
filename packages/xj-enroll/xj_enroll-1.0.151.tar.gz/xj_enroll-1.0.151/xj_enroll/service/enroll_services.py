"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: CURD 工具
@created_time: 2022/9/15 14:14
"""
from pathlib import Path

from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from django.db.models import F

from main.settings import BASE_DIR
from xj_finance.services.finance_transacts_service import FinanceTransactsService
from ..models import Enroll, EnrollRecord, EnrollSubitem
from ..service.clock_service import ClockService
from ..service.enroll_record_serivce import EnrollRecordServices
from ..service.enroll_subitem_record_service import EnrollSubitemRecordService
from ..service.subitem_extend_service import output_convert
from ..utils.custom_tool import format_params_handle, write_to_log
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))

sand_box_meet = main_config_dict.sand_box_meet or module_config_dict.sand_box_meet or ""
sand_box_receivable = main_config_dict.sand_box_receivable or module_config_dict.sand_box_receivable or ""


class EnrollServices:
    def __init__(self):
        pass

    @staticmethod
    def enroll_add(params, subitem=None):
        """
        报名表新增
        :param params:
        :return: data,err
        """
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "thread_id", "user_id", "category_id", "trading_relate", "region_code", "occupy_room",
                "enroll_status_code", "enroll_status_code_id",
                "min_number", "max_number", "min_count_apiece", "max_count_apiece", "enroll_rule_group_id",
                "enroll_rule_group", "price", "count", "unit", "fee", "reduction", "subitems_amount", "amount",
                "paid_amount", "unpaid_amount", "commision", "deposit",
                "hide_price", "hide_user", "has_repeat", "has_subitem", "has_audit", "has_vouch", "need_deposit",
                "need_imprest", "enable_pool",
                "pool_limit", "pool_stopwatch", "open_time", "close_time", "launch_time", "finish_time", "spend_time",
                "create_time", "update_time", "snapshot", "remark", "finance_invoicing_code"
            ],
        )

        try:
            instance = Enroll.objects.create(**params)
        except Exception as e:
            return None, str(e)

        return instance.to_json(), None

    @staticmethod
    def enroll_detail(enroll_id, user_id=None, simple_return=False):
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return None, "不存的报名信息"
        enroll_detail = enroll_obj.first().to_json()

        # 是否输出联表数据
        if not simple_return:
            # 报名倒计时
            # clocker = ClockService()
            # data, err = clocker.check_clock(enroll_id)
            # enroll_detail.update(data)

            # 当前用户是否存在报名记录/当前用户是否存在报名分项记录
            enroll_detail["this_user_has_record"] = 0
            enroll_detail["this_user_has_subitem_record"] = 0

            # 获取需要拼接的数据，报名分项，报名记录，报名分项记录
            enroll_subitems_record_list, err = EnrollSubitemRecordService.list({"enroll_id": enroll_id}, False)
            main_record_list, err = EnrollRecordServices.record_list({"enroll_id": enroll_id}, need_pagination=False)
            # 报名分项列表 进行扩展字段转换
            enroll_subitems_list = output_convert(list(EnrollSubitem.objects.annotate(category_id=F("enroll__category_id")).filter(enroll_id=enroll_id).values()))

            # 获取报名分你想记录的记录映射 {"enroll_record_id":item}
            record_id_to_subitems_record_map = {}
            for enroll_subitems_record in enroll_subitems_record_list:
                this_subitems_record = record_id_to_subitems_record_map.get(
                    enroll_subitems_record["enroll_record_id"],
                    None
                )
                if not this_subitems_record:
                    record_id_to_subitems_record_map[enroll_subitems_record["enroll_record_id"]] = [enroll_subitems_record]
                    continue
                this_subitems_record.append(enroll_subitems_record)

            # 获取报名分你想记录的记录映射 {"enroll_subitem_id":item}
            subitems_id_to_subitem_record_map = {}
            for enroll_subitems_record in enroll_subitems_record_list:
                this_subitems_record = subitems_id_to_subitem_record_map.get(
                    enroll_subitems_record["enroll_subitem_id"], None)
                if not this_subitems_record:
                    subitems_id_to_subitem_record_map[enroll_subitems_record["enroll_subitem_id"]] = [enroll_subitems_record]
                    continue
                this_subitems_record.append(enroll_subitems_record)

            # 判断当前用户是否存在报名分项记录
            for enroll_subitems_record_item in enroll_subitems_record_list:
                if not enroll_subitems_record_item["user_id"] or not enroll_subitems_record_item["user_id"] == user_id:
                    continue
                enroll_detail["this_user_has_subitem_record"] = 1

            # 报名记录和报名分项记录进行数据拼接
            for main_record in main_record_list:
                main_record["subitem_record_list"] = record_id_to_subitems_record_map.get(main_record["id"], {})
                if main_record["user_id"] and main_record["user_id"] == user_id:
                    enroll_detail["this_user_has_record"] = 1
            enroll_detail["subitem_list"] = enroll_subitems_list

            for enroll_subitem in enroll_subitems_list:
                enroll_subitem["subitem_record_list"] = subitems_id_to_subitem_record_map.get(enroll_subitem["id"], {})
            enroll_detail["main_record_list"] = main_record_list

        return enroll_detail, None

    @staticmethod
    def enroll_list(params, filter_fields=None, need_pagination=True):
        # 字段处理
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        filter_fields_list = filter_fields.split(";") if filter_fields else []
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id", "id_list|list", "thread_id", "category_id", "category_id_list|list", "thread_id_list|list",
                "trading_relate", "region_code", "spend_time_start",
                "enroll_status_code", "enroll_status_code_list|list",
                "spend_time_end", "create_time_start", "create_time_end", "finish_time_start", "finish_time_end",
                "open_time_start", "open_time_end", "enroll_status_code", "has_subitem", "finance_invoicing_code"
            ],
            split_list=["category_id_list", "id_list", "enroll_status_code_list", "thread_id_list"],
            alias_dict={
                "spend_time_start": "spend_time__gte", "spend_time_end": "spend_time__lte",
                "create_time_start": "create_time__gte", "create_time_end": "create_time__lte",
                "finish_time_start": "finish_time__gte", "open_time_start": "open_time__gte",
                "open_time_end": "open_time__lte", "enroll_classify_value": "classify__value",
                "enroll_category_value": "category__value",
                "thread_id_list": "thread_id__in", "category_id_list": "category_id__in", "id_list": "id__in",
                "enroll_status_code_list": "enroll_status_code__in"
            },
        )
        enroll_obj = Enroll.objects.filter(**params).order_by("-id").values(*filter_fields_list)
        if not need_pagination:
            return list(enroll_obj), None

        # 分页展示
        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
        except EmptyPage:
            enroll_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            return None, f'{str(e)}'
        return {'total': paginator.count, "page": page, "size": size, 'list': list(enroll_obj.object_list)}, None

    @staticmethod
    def enroll_own_list(params, need_pagination=True):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "enroll_id", "thread_id", "user_id", "enroll_pay_status", "enroll_status_code", "enroll_status_code_list",
                "price", "count", "amount", "category_id", "thread_id_list", "finance_invoicing_code"
            ],
            split_list=["enroll_status_code_list"],
            alias_dict={"enroll_id": "id", "enroll_status_code_list": "enroll_status_code__in", "thread_id_list": "thread_id__in"}
        )
        enroll_obj = Enroll.objects.filter(**params).order_by("-id").values()
        if not need_pagination:
            # serializer = EnrollRecordListSerializer(data=enroll_obj)
            # serializer.is_valid()
            return list(enroll_obj.object_list), None

        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
        except EmptyPage:
            enroll_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            return None, f'{str(e)}'
        return {'total': paginator.count, "page": page, "size": size, 'list': list(enroll_obj.object_list)}, None

    @staticmethod
    def enroll_undertake_list(params, need_pagination=True):
        size = params.pop('size', 10)
        page = params.pop('page', 1)

        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "enroll_id", "category_id", "thread_id_list", "user_id", "enroll_pay_status", "enroll_status_code",
                "enroll_status_code_list", "price", "count", "amount", "finance_invoicing_code"
            ],
            split_list=["enroll_status_code_list"],
            alias_dict={
                "enroll_status_code_list": "enroll_status_code__in",
                "thread_id_list": "enroll__thread_id__in",
                "category_id": "enroll__category_id"
            }
        )
        enroll_obj = EnrollRecord.objects.annotate(
            commision=F("enroll__commision"),
            thread_id=F("enroll__thread_id")
        ).filter(**params).order_by("-id").values()

        if not need_pagination:
            # 扩展字段替换，并过滤
            return EnrollRecordServices.extend_transform_fields(list(enroll_obj.object_list)), None

        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
        except EmptyPage:
            enroll_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            return None, f'{str(e)}'

        # 扩展字段替换，并过滤
        enroll_record_list = EnrollRecordServices.extend_transform_fields(list(enroll_obj.object_list))
        return {'total': paginator.count, "page": page, "size": size, 'list': enroll_record_list}, None

    @staticmethod
    def enroll_edit(params: dict = None, enroll_id=None, search_param: dict = None):
        if not search_param:
            search_param = {}

        # 搜索字段过滤
        search_param = format_params_handle(
            param_dict=search_param,
            filter_filed_list=[
                "enroll_id_list", "thread_id", "thread_id_list", "category_id", "category_id_list", "trading_relate", "region_code",
                "enroll_status_code", "enroll_rule_group", "enroll_rule_group_id",
            ],
            alias_dict={"enroll_id_list": "id__in", "thread_id_list": "thread_id__in"}
        )

        if not enroll_id and not search_param:
            return None, "无法找到要修改数据，请检查参数"

        enroll_id = params.pop("enroll_id", None) or enroll_id
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "thread_id", "category_id", "trading_relate", "region_code", "occupy_room", "enroll_status_code",
                "min_number", "max_number", "min_count_apiece", "max_count_apiece",
                "enroll_rule_group", "price", "count", "unit", "fee", "reduction", "subitems_amount", "amount",
                "paid_amount", "unpaid_amount", "commision", "deposit",
                "bid_mode", "ticket", "hide_price", "hide_user", "has_repeat", "has_subitem", "has_audit", "has_vouch",
                "need_deposit", "need_imprest", "enable_pool",
                "pool_limit", "pool_stopwatch", "open_time", "close_time", "launch_time", "finish_time", "spend_time",
                "create_time", "update_time", "snapshot", "remark", "finance_invoicing_code"
            ],
        )
        # print("enroll_id:", enroll_id, "search_param:", search_param, "params:", params)
        if not params:
            return None, "没有可修改的内容"

        enroll_obj = Enroll.objects
        if enroll_id:
            enroll_obj = enroll_obj.filter(id=enroll_id)
        if search_param:
            enroll_obj = enroll_obj.filter(**search_param)
        if not enroll_obj:
            return None, None
        try:
            enroll_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return enroll_obj.first().to_json(), None

    @staticmethod
    def enroll_delete(enroll_id):
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return None, None
        try:
            enroll_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def enroll(request_params=None):
        """报名记录联合添加报名记录和分项记录"""
        sid = transaction.savepoint()
        # 信息主表
        main_record_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=[
                "id", "enroll_id", "user_id", "enroll_auth_status_id", "enroll_pay_status_id", "enroll_status_code",
                "create_time", "price", "deposit", "count",
                "main_amount", "coupon_amount", "again_reduction", "subitems_amount", "deposit_amount", "amount",
                "paid_amount", "unpaid_amount", "fee", "photos",
                "files", "score", "reply", "remark",
            ]
        )
        main_data, err = EnrollRecordServices.record_add(main_record_params)
        if err:
            transaction.savepoint_rollback(sid)
            return None, err

        # 分项表
        subitem_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["enroll_record_id", "enroll_subitem_id", "user_id", "subitem_price", "subitem_count",
                               "subitem_amount", ],
            alias_dict={"subitem_price": "price", "subitem_count": "count"}
        )

        enroll_record_id = main_data.get("id", None)
        if not enroll_record_id:
            transaction.savepoint_rollback(sid)
            return None, err
        subitem_params["enroll_record_id"] = enroll_record_id

        subitem_data, err = EnrollSubitemRecordService.add(subitem_params)
        if err:
            transaction.savepoint_rollback(sid)
            return None, err

        # 添加定时器
        clocker = ClockService()
        clocker.add_clock(enroll_id=request_params.get("enroll_id"), user_id=request_params.get("user_id"))
        transaction.clean_savepoints()
        return None, err

    @staticmethod
    def bxtx_pay_call_back(order_no):
        """
        镖行天下支付业务回调服务
        回调逻辑：
        1.用户支付分为两种：（1）用户支付预付款 （2）用户补差价
        情况1：支付预付款，但是还没有成单。修改状态进入代报名状态。
        情况2：（报名并指派后）用户支付差价，订单开始。进入上传状态。
        扩展逻辑：分销逻辑，资金逻辑。

        2023-2-6 回调逻辑：第一种代补差价付款成功后，直接进入已接单待上传，第二种：付完首付款后直接进入报名中
        :param order_no: 订单号
        :return: response
        """
        try:
            finance_transact_data, err = FinanceTransactsService.detail(order_no=order_no)
            if err:
                raise Exception(err)

            user_id = finance_transact_data.get("account_id", None)
            enroll_id = finance_transact_data.get("enroll_id", None)
            outgo = finance_transact_data.get("outgo", 0)
            # print("支付回调报名", "user_id:", user_id, "enroll_id:", enroll_id, "order_no", order_no)
            # enroll_obj = Enroll.objects.filter(id=enroll_id, user_id=user_id)
            enroll_obj = Enroll.objects.filter(id=enroll_id)
            enroll_set = enroll_obj.first()
            if not enroll_set:
                return None, None
            paid_amount = (enroll_set.paid_amount or 0) + (outgo or 0)
            # print(paid_amount, enroll_set.enroll_status_code)
            if int(enroll_set.enroll_status_code) == 243:
                enroll_obj.update(paid_amount=paid_amount, unpaid_amount=0, enroll_status_code=356)
                EnrollSubitem.objects.filter(enroll_id=enroll_id).update(enroll_subitem_status_code=356)
                enroll_status_code = 356
            else:
                enroll_obj.update(paid_amount=paid_amount, unpaid_amount=0, enroll_status_code=232)
                EnrollSubitem.objects.filter(enroll_id=enroll_id).update(enroll_subitem_status_code=232)
                enroll_status_code = 232
            # EnrollRecord.objects.filter(enroll_id=enroll_id).update(enroll_status_code=43)

            # 写入资金沙盒
            pass

            return enroll_status_code, None
        except Exception as e:
            write_to_log(prefix="报名支付回调异常", content="order_no:" + str(order_no or ""), err_obj=e)
            return None, e

    @staticmethod
    def enroll_check_and_accept(enroll_id=None, check_success_code=656, **kwargs):
        """
        报名余额验收中
        :param enroll_id: 报名ID
        :param check_success_code: 当前审核中的状态码
        :param kwargs:  **
        :return:data,err
        """
        # print("enroll_id:", enroll_id, "check_success_code:", check_success_code)
        if not enroll_id or check_success_code is None:
            return None, "参数错误"
        is_check_success = Enroll.objects.filter(id=enroll_id, enroll_status_code=check_success_code).values("id").first()
        if not is_check_success:
            return None, "该报名不可触发余额"
        try:
            # ============ 完成订单联动资金修改 start ============
            # TODO 资金联动代码块，后期使用流程控制
            records_vales = list(
                EnrollRecord.objects.filter(enroll_id=enroll_id, enroll_status_code=check_success_code).values(
                    "user_id", "price", 'again_price', "initiator_again_price"
                )
            )
            for item in records_vales:
                write_to_log(prefix="资金联动修改：", content={
                    "account_id": item.get("user_id"),
                    "amount": item.get("again_price", 0),
                    "currency": "CNY",
                    "pay_mode": "BALANCE",
                    "enroll_id": enroll_id
                })
                FinanceTransactsService.finance_create_or_write_off(data={
                    "account_id": item.get("user_id"),
                    "amount": item.get("again_price", 0),
                    "currency": "CNY",
                    "pay_mode": "BALANCE",
                    "enroll_id": enroll_id
                })
            # ============ 完成订单联动资金修改 end ============
        except Exception as e:
            write_to_log(prefix="资金联动修改：", err_obj=e)
