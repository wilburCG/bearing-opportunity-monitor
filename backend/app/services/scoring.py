PRIORITY_INDUSTRIES = {"风电", "钢铁", "矿山", "水泥", "轨交"}


def compute_total_score(volume_score: float, urgency_score: float, confidence_score: float, fit_score: float) -> float:
    """机会综合评分 v1。

    权重后续可根据销售反馈调整。
    """
    return round(
        volume_score * 0.35
        + urgency_score * 0.25
        + confidence_score * 0.25
        + fit_score * 0.15,
        2,
    )


def compute_fit_score(industry: str | None) -> float:
    if not industry:
        return 40
    return 90 if industry in PRIORITY_INDUSTRIES else 60
