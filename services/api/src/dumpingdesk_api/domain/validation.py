from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from statistics import mean, pstdev

from dumpingdesk_api.domain.models import CostOfProduction, ProceedingConfig, USSale, ValidationEvent


def validate_matter_data(
    config: ProceedingConfig,
    *,
    us_sales: list[USSale],
    costs: list[CostOfProduction] | None = None,
) -> list[ValidationEvent]:
    costs = costs or []
    events: list[ValidationEvent] = []
    events.extend(_validate_required_us_sale_fields(us_sales))
    events.extend(_validate_period(config, us_sales))
    events.extend(_validate_costs(us_sales, costs))
    events.extend(_validate_price_outliers(us_sales))
    return events


def _validate_required_us_sale_fields(us_sales: list[USSale]) -> list[ValidationEvent]:
    events: list[ValidationEvent] = []
    for sale in us_sales:
        if not sale.invoice_id:
            events.append(
                ValidationEvent(
                    code="MISSING_REQUIRED_FIELD",
                    severity="BLOCKING",
                    message="U.S. sale is missing invoice ID.",
                    record_id=sale.invoice_id or None,
                    field="invoice_id",
                )
            )
        if not sale.connum:
            events.append(
                ValidationEvent(
                    code="MISSING_REQUIRED_FIELD",
                    severity="BLOCKING",
                    message="U.S. sale is missing CONNUM.",
                    record_id=sale.invoice_id,
                    field="connum",
                )
            )
        if sale.quantity <= 0:
            events.append(
                ValidationEvent(
                    code="NON_POSITIVE_QUANTITY",
                    severity="ERROR",
                    message="U.S. sale quantity must be greater than zero.",
                    record_id=sale.invoice_id,
                    field="quantity",
                )
            )
    return events


def _validate_period(config: ProceedingConfig, us_sales: list[USSale]) -> list[ValidationEvent]:
    events: list[ValidationEvent] = []
    for sale in us_sales:
        if sale.sale_date < config.period_start or sale.sale_date > config.period_end:
            events.append(
                ValidationEvent(
                    code="SALE_DATE_OUTSIDE_PERIOD",
                    severity="ERROR",
                    message="U.S. sale date falls outside the configured POR.",
                    record_id=sale.invoice_id,
                    field="sale_date",
                )
            )
    return events


def _validate_costs(
    us_sales: list[USSale],
    costs: list[CostOfProduction],
) -> list[ValidationEvent]:
    events: list[ValidationEvent] = []
    cost_connums = {cost.connum for cost in costs}
    for connum in sorted({sale.connum for sale in us_sales} - cost_connums):
        events.append(
            ValidationEvent(
                code="MISSING_COST_COVERAGE",
                severity="BLOCKING",
                message=f"U.S.-sold CONNUM {connum} has no cost record.",
                field="connum",
            )
        )

    for cost in costs:
        if cost.variable_cost <= 0 or cost.fixed_cost < 0 or cost.total_cost <= 0:
            events.append(
                ValidationEvent(
                    code="NON_POSITIVE_COST",
                    severity="BLOCKING",
                    message=f"Cost record for CONNUM {cost.connum} has non-positive cost values.",
                    record_id=cost.connum,
                    field="cost",
                )
            )
    return events


def _validate_price_outliers(us_sales: list[USSale]) -> list[ValidationEvent]:
    events: list[ValidationEvent] = []
    grouped: dict[str, list[USSale]] = defaultdict(list)
    for sale in us_sales:
        grouped[sale.connum].append(sale)

    for connum, sales in grouped.items():
        if len(sales) < 3:
            continue
        prices = [float(sale.net_unit_price) for sale in sales]
        standard_deviation = pstdev(prices)
        if standard_deviation == 0:
            continue
        average = mean(prices)
        for sale in sales:
            z_score = abs((float(sale.net_unit_price) - average) / standard_deviation)
            if Decimal(str(z_score)) > Decimal("3"):
                events.append(
                    ValidationEvent(
                        code="PRICE_OUTLIER",
                        severity="WARNING",
                        message=f"Sale price for CONNUM {connum} is more than 3 sigma from cohort.",
                        record_id=sale.invoice_id,
                        field="net_unit_price",
                    )
                )
    return events
