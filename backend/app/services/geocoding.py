"""Geocoding helpers for opportunity locations.

Primary path: AMap/Gaode geocoding API when GAODE_API_KEY is configured.
Fallback path: deterministic China province/city center coordinates so records with
province/city can still appear on the opportunity map.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

import httpx

from app.core.config import settings


@dataclass(frozen=True)
class GeocodeResult:
    latitude: float
    longitude: float
    source: str
    matched_name: str | None = None


# City centers are approximate and intended as a fallback marker location only.
# Prefer precise geocoding via AMap when a key is configured.
CITY_CENTERS: dict[str, tuple[float, float]] = {
    "北京": (39.9042, 116.4074),
    "北京市": (39.9042, 116.4074),
    "天津": (39.3434, 117.3616),
    "天津市": (39.3434, 117.3616),
    "上海": (31.2304, 121.4737),
    "上海市": (31.2304, 121.4737),
    "重庆": (29.5630, 106.5516),
    "重庆市": (29.5630, 106.5516),
    "银川": (38.4872, 106.2309),
    "银川市": (38.4872, 106.2309),
    "三明": (26.2654, 117.6389),
    "三明市": (26.2654, 117.6389),
    "吉林": (43.8378, 126.5496),
    "吉林市": (43.8378, 126.5496),
    "遵义": (27.7257, 106.9274),
    "遵义市": (27.7257, 106.9274),
    "洛阳": (34.6197, 112.4540),
    "洛阳市": (34.6197, 112.4540),
    "长沙": (28.2282, 112.9388),
    "长沙市": (28.2282, 112.9388),
    "西宁": (36.6171, 101.7782),
    "西宁市": (36.6171, 101.7782),
    "聊城": (36.4567, 115.9854),
    "聊城市": (36.4567, 115.9854),
    "邯郸": (36.6256, 114.5391),
    "邯郸市": (36.6256, 114.5391),
}

PROVINCE_CENTERS: dict[str, tuple[float, float]] = {
    "北京": (39.9042, 116.4074),
    "北京市": (39.9042, 116.4074),
    "天津": (39.3434, 117.3616),
    "天津市": (39.3434, 117.3616),
    "河北": (38.0428, 114.5149),
    "河北省": (38.0428, 114.5149),
    "山西": (37.8706, 112.5489),
    "山西省": (37.8706, 112.5489),
    "辽宁": (41.8057, 123.4315),
    "辽宁省": (41.8057, 123.4315),
    "吉林": (43.8378, 126.5496),
    "吉林省": (43.8378, 126.5496),
    "黑龙江": (45.7422, 126.6617),
    "黑龙江省": (45.7422, 126.6617),
    "上海": (31.2304, 121.4737),
    "上海市": (31.2304, 121.4737),
    "江苏": (32.0603, 118.7969),
    "江苏省": (32.0603, 118.7969),
    "浙江": (30.2741, 120.1551),
    "浙江省": (30.2741, 120.1551),
    "安徽": (31.8206, 117.2272),
    "安徽省": (31.8206, 117.2272),
    "福建": (26.0745, 119.2965),
    "福建省": (26.0745, 119.2965),
    "江西": (28.6829, 115.8582),
    "江西省": (28.6829, 115.8582),
    "山东": (36.6512, 117.1201),
    "山东省": (36.6512, 117.1201),
    "河南": (34.7657, 113.7536),
    "河南省": (34.7657, 113.7536),
    "湖北": (30.5928, 114.3055),
    "湖北省": (30.5928, 114.3055),
    "湖南": (28.2282, 112.9388),
    "湖南省": (28.2282, 112.9388),
    "Hunan": (28.2282, 112.9388),
    "广东": (23.1291, 113.2644),
    "广东省": (23.1291, 113.2644),
    "广西": (22.8170, 108.3669),
    "广西壮族自治区": (22.8170, 108.3669),
    "海南": (20.0440, 110.1999),
    "海南省": (20.0440, 110.1999),
    "重庆": (29.5630, 106.5516),
    "重庆市": (29.5630, 106.5516),
    "四川": (30.5728, 104.0668),
    "四川省": (30.5728, 104.0668),
    "贵州": (26.6470, 106.6302),
    "贵州省": (26.6470, 106.6302),
    "云南": (25.0389, 102.7183),
    "云南省": (25.0389, 102.7183),
    "陕西": (34.3416, 108.9398),
    "陕西省": (34.3416, 108.9398),
    "甘肃": (36.0611, 103.8343),
    "甘肃省": (36.0611, 103.8343),
    "青海": (36.6171, 101.7782),
    "青海省": (36.6171, 101.7782),
    "Qinghai": (36.6171, 101.7782),
    "宁夏": (38.4872, 106.2309),
    "宁夏回族自治区": (38.4872, 106.2309),
    "新疆": (43.8256, 87.6168),
    "新疆维吾尔自治区": (43.8256, 87.6168),
    "内蒙古": (40.8426, 111.7492),
    "内蒙古自治区": (40.8426, 111.7492),
}

# Last-resort inference for legacy/imported records where province/city/address were missing
# but the company or title contains a recognizable place/customer name.
KEYWORD_CENTERS: dict[str, tuple[float, float, str]] = {
    "天津铁厂": (36.6256, 114.5391, "邯郸/天津铁厂线索兜底"),
    "鲁西集团": (36.4567, 115.9854, "聊城/鲁西集团"),
    "Luxi Group": (36.4567, 115.9854, "聊城/鲁西集团"),
    "湘澧盐化": (28.2282, 112.9388, "长沙/湖南线索兜底"),
    "Zhongfu Shenying": (36.6171, 101.7782, "西宁/中复神鹰"),
}


def compact_parts(parts: Iterable[str | None]) -> list[str]:
    return [str(x).strip() for x in parts if x and str(x).strip()]


def build_address(*parts: str | None) -> str:
    return " ".join(compact_parts(parts))


def _normalize_location_key(value: str | None) -> str | None:
    if not value:
        return None
    text = str(value).strip()
    if not text:
        return None
    # Remove common suffixes progressively when direct match fails.
    return text


def _lookup_center(name: str | None, centers: dict[str, tuple[float, float]]) -> tuple[float, float] | None:
    key = _normalize_location_key(name)
    if not key:
        return None
    if key in centers:
        return centers[key]
    simplified = re.sub(r"(省|市|地区|回族自治区|维吾尔自治区|壮族自治区|自治区)$", "", key)
    return centers.get(simplified)


async def geocode_with_amap(address: str, city: str | None = None) -> GeocodeResult | None:
    key = (settings.gaode_api_key or "").strip()
    if not key or not address.strip():
        return None
    params = {"key": key, "address": address.strip()}
    if city:
        params["city"] = city
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get("https://restapi.amap.com/v3/geocode/geo", params=params)
            response.raise_for_status()
            payload = response.json()
    except Exception:
        return None

    if payload.get("status") != "1" or not payload.get("geocodes"):
        return None
    location = payload["geocodes"][0].get("location")
    if not location or "," not in location:
        return None
    lng_text, lat_text = location.split(",", 1)
    try:
        return GeocodeResult(
            latitude=float(lat_text),
            longitude=float(lng_text),
            source="amap",
            matched_name=payload["geocodes"][0].get("formatted_address"),
        )
    except ValueError:
        return None


def geocode_with_fallback(
    *,
    province: str | None = None,
    city: str | None = None,
    address: str | None = None,
    company_name: str | None = None,
    title: str | None = None,
) -> GeocodeResult | None:
    city_center = _lookup_center(city, CITY_CENTERS)
    if city_center:
        lat, lng = city_center
        return GeocodeResult(lat, lng, "fallback_city", city)

    # Some records put a city-like token into province.
    province_as_city_center = _lookup_center(province, CITY_CENTERS)
    if province_as_city_center:
        lat, lng = province_as_city_center
        return GeocodeResult(lat, lng, "fallback_city", province)

    province_center = _lookup_center(province, PROVINCE_CENTERS)
    if province_center:
        lat, lng = province_center
        return GeocodeResult(lat, lng, "fallback_province", province)

    haystack = " ".join(compact_parts([address, company_name, title]))
    for keyword, (lat, lng, matched) in KEYWORD_CENTERS.items():
        if keyword in haystack:
            return GeocodeResult(lat, lng, "fallback_keyword", matched)

    return None


async def geocode_opportunity_location(
    *,
    province: str | None = None,
    city: str | None = None,
    district: str | None = None,
    address: str | None = None,
    company_name: str | None = None,
    title: str | None = None,
) -> GeocodeResult | None:
    query = build_address(province, city, district, address, company_name)
    result = await geocode_with_amap(query, city=city or province)
    if result:
        return result
    return geocode_with_fallback(
        province=province,
        city=city,
        address=address,
        company_name=company_name,
        title=title,
    )
