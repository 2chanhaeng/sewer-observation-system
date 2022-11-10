from typing import Final
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
import environ
from .models import Gu
from datetime import datetime, timedelta
import requests

ResponseData = dict[str, float | str]
ResponseDataRow = list[ResponseData]
ResponseResult = dict[str, str]
SuccessedResponse = dict[str, int | ResponseResult | ResponseDataRow]
FailedResponse = dict[str, ResponseResult] | dict[None, None]

environ.Env.read_env(".env")
env = environ.Env(DEBUG=(bool, False))

TIMEZONE = "Asia/Seoul"
API_URL_BASE = "http://openapi.seoul.go.kr:8088/"
API_URL_SEWAGE = API_URL_BASE + "{}/json/DrainpipeMonitoringInfo/{}/{}/{}/{}/{}/"
API_URL_RAINFALL = API_URL_BASE + "{}/json/ListRainfallService/{}/{}/{}/"


def req(url: str, *formats) -> SuccessedResponse | FailedResponse:
    """
    URL에 인자와 API 키를 넣어서 요청을 보내 응답을 반환.
    """
    res = requests.get(url.format(env("SEOUL_OPEN_API_KEY"), *formats))
    if res.status_code != 200:
        return {}
    try:
        return res.json()
    except Exception:
        return {}


@api_view(["GET"])
def rainfall_sewage_view(request: Request, gubn: str) -> Response:
    """
    GET /data/<str:gubn>/
    실시간 강수량, 하수관 데이터를 응답.
    """
    if request.method == "GET":
        if len(gubn) < 2:
            gubn = "0" + gubn
        gu = get_object_or_404(Gu, gubn=gubn)  # gubn 으로 구 데이터 검색
        res_data = {}  # 반환할 데이터
        rg_count: int = gu.rainguage_set.count()  # 우량계 개수
        rf_res = req(API_URL_RAINFALL, 1, rg_count, gu.name)  # 강수량 데이터 요청
        # 이 떄, 우량계 데이터 만큼의 데이터를 요청하여 우량계 별 가장 최신의 데이터를 가져옴
        rf_data = rf_res.get("ListRainfallService")  # 강수량 데이터 있는지 확인
        if rf_data:  # 강수량 데이터가 있으면
            res_data["rainfall"] = rf_data.get("row")  # 실제 데이터를 반환할 데이터에 저장

        """
        하수관 데이터는 한 시간 단위로 불러올 수 있음.
        예: 22시 데이터까지 요청하면 22:59까지의 데이터를 가져옴.
        또한 데이터가 즉각 올라오지 않기 때문에
        00~10분 사이에는 데이터가 제대로 불러와지지 않음.
        따라서 최신 데이터를 가져오기 위해서는 다음과 같은 과정이 필요함.
        1. 한 시간 전부터 현재 시각까지의 데이터를 하나만 요청.
        2. 응답에서 한시간 전~현재시각의 데이터 개수만 확인.
        3. 이후 동일한 시간의 데이터를 가져오는데,
            이때 최대 인덱스를 2에서 추출한 데이터 개수,
            최소 인덱스를 데이터 개수에서 하수관 개수를 뺀 값으로 설정.
        이런 식으로 하수관 별 최신 데이터만 취득.
        """
        now: Final = datetime.now().strftime("%Y%m%d%H")  # 현재 시간
        ahourago: Final = (datetime.now() - timedelta(hours=1)).strftime("%Y%m%d%H")
        # 1시간 전 시간
        sw_count: int = gu.sewer_set.count()
        sw_res = req(API_URL_SEWAGE, 1, 1, gubn, ahourago, now)  # 하수관 데이터를 하나만 요청
        sw_data = sw_res.get("DrainpipeMonitoringInfo")  # 하수관 데이터 추출
        if sw_data and sw_data.get("list_total_count"):  # 하수관 데이터가 있으면
            end: int = sw_data["list_total_count"]  # 데이터 총 개수
            start: int = end - sw_count
            # 데이털 총 개수에서 하수관 개수를 뺀 값
            sw_res = req(  # 하수관 데이터 요청
                API_URL_SEWAGE,
                start,
                end,
                gubn,
                ahourago,
                now,
            )
            sw_res_data: dict = sw_res.get("DrainpipeMonitoringInfo")
            # 하수관 데이터 있는지 확인
            if sw_res_data:  # 하수관 데이터가 있다면
                res_data["sewage"] = sw_res_data.get("row")
                # 실제 데이터를 반환할 데이터에 저장
        return Response(res_data, status=200) if res_data else Response(status=404)
        # 데이터가 있으면 데이터를 반환, 없으면 404 반환
    return Response(status=400)  # 잘못된 요청이면 400 반환
