from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP, getcontext

from dumpingdesk_api.domain.models import (
    HomeMarketSale,
    MarginCalculationResult,
    MarginLine,
    ProceedingConfig,
    USSale,
)

getcontext().prec = 28

SIX_PLACES = Decimal("0.000001")


def calculate_ad_margin(
    config: ProceedingConfig,
    us_sales: list[USSale],
    home_market_sales: list[HomeMarketSale],
) -> MarginCalculationResult:
    normal_values = _normal_values_by_connum(home_market_sales)
    lines: list[MarginLine] = []

    for sale in us_sales:
        normal_value = normal_values.get(sale.connum)
        if normal_value is None:
            continue
        margin = _quantize((normal_value - sale.net_unit_price) / sale.net_unit_price)
        dumping_amount = (normal_value - sale.net_unit_price) * sale.quantity
        if not config.zeroing or dumping_amount > 0:
            weighted_dumping_amount = dumping_amount
        else:
            weighted_dumping_amount = Decimal("0")
        lines.append(
            MarginLine(
                invoice_id=sale.invoice_id,
                connum=sale.connum,
                normal_value=normal_value,
                us_net_price=sale.net_unit_price,
                quantity=sale.quantity,
                margin=margin,
                dumping_amount=weighted_dumping_amount,
            )
        )

    total_us_value = sum((line.us_net_price * line.quantity for line in lines), Decimal("0"))
    total_dumping = sum((line.dumping_amount for line in lines), Decimal("0"))
    weighted_average_margin = _quantize(total_dumping / total_us_value) if total_us_value else Decimal("0")

    return MarginCalculationResult(
        matter_id=config.matter_id,
        weighted_average_margin=weighted_average_margin,
        normal_values_by_connum=normal_values,
        lines=lines,
    )


def _normal_values_by_connum(home_market_sales: list[HomeMarketSale]) -> dict[str, Decimal]:
    grouped: dict[str, list[HomeMarketSale]] = defaultdict(list)
    for sale in home_market_sales:
        grouped[sale.connum].append(sale)

    normal_values: dict[str, Decimal] = {}
    for connum, sales in grouped.items():
        total_quantity = sum((sale.quantity for sale in sales), Decimal("0"))
        if total_quantity == 0:
            continue
        total_value = sum((sale.net_unit_price * sale.quantity for sale in sales), Decimal("0"))
        normal_values[connum] = _quantize(total_value / total_quantity)
    return normal_values


def _quantize(value: Decimal) -> Decimal:
    return value.quantize(SIX_PLACES, rounding=ROUND_HALF_UP)
