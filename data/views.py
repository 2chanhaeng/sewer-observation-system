from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
import environ
from .models import Gu
from datetime import datetime, timedelta
import requests


environ.Env.read_env(".env")
env = environ.Env(DEBUG=(bool, False))
API_KEY = env("SEOUL_OPEN_API_KEY")

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


# 정해진 기간 동안의 강수량을 반환하는 API
@api_view(["GET"])
def rainfall_sewage_view(request: Request, gubn: str) -> Response:
    if request.method == "GET":
        if len(gubn) < 2:
            gubn = "0" + gubn
        gu = get_object_or_404(Gu, gubn=gubn)
        res_data = {}
        rg_count = gu.rainguage_set.count()
        rf_res = req(API_URL_RAINFALL, 1, rg_count, gu.name)
        rf_data = rf_res.get("ListRainfallService")
        if rf_data:
            res_data["rainfall"] = rf_data.get("row")
        now = datetime.now().strftime("%Y%m%d%H")
        ahourago = (datetime.now() - timedelta(hours=1)).strftime("%Y%m%d%H")
        sw_res = req(API_URL_SEWAGE, 1, 1, gubn, ahourago, now)
        sw_data = sw_res.get("DrainpipeMonitoringInfo")
        if sw_data:
            end: int = sw_data["list_total_count"]
            start: int = end - gu.sewer_set.count()
            sw_res = req(
                API_URL_SEWAGE,
                start,
                end,
                gubn,
                ahourago,
                now,
            )
            sw_res_data: dict = sw_res.get("DrainpipeMonitoringInfo")
            if sw_res_data:
                res_data["sewage"] = sw_res_data.get("row")
        return Response(res_data, status=200) if res_data else Response(status=404)
    return Response(status=400)
