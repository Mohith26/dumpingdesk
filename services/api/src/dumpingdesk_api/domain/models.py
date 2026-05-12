from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import Any, Literal


class DatasetKind(StrEnum):
    US_SALES = "us_sales"
    HOME_MARKET_SALES = "home_market_sales"
    COSTS = "costs"


Severity = Literal["INFO", "WARNING", "ERROR", "BLOCKING"]


@dataclass(frozen=True)
class ProceedingConfig:
    matter_id: str
    case_number: str
    period_start: date
    period_end: date
    proceeding_type: str = "AD"
    segment: str = "admin_review"
    comparison_methodology: str = "W_to_W"
    zeroing: bool = False
    methodology_version: str = "2024.3"


@dataclass(frozen=True)
class SaleRecord:
    invoice_id: str
    connum: str
    gross_unit_price: Decimal
    quantity: Decimal
    sale_date: date
    currency: str = "USD"
    movement_expense: Decimal = Decimal("0")
    direct_selling_expense: Decimal = Decimal("0")
    packing_expense: Decimal = Decimal("0")

    @property
    def net_unit_price(self) -> Decimal:
        return (
            self.gross_unit_price
            - self.movement_expense
            - self.direct_selling_expense
            - self.packing_expense
        )

    @property
    def net_sales_value(self) -> Decimal:
        return self.net_unit_price * self.quantity


@dataclass(frozen=True)
class USSale(SaleRecord):
    pass


@dataclass(frozen=True)
class HomeMarketSale(SaleRecord):
    pass


@dataclass(frozen=True)
class CostOfProduction:
    connum: str
    variable_cost: Decimal
    fixed_cost: Decimal
    currency: str = "USD"

    @property
    def total_cost(self) -> Decimal:
        return self.variable_cost + self.fixed_cost


@dataclass(frozen=True)
class ValidationEvent:
    code: str
    severity: Severity
    message: str
    record_id: str | None = None
    field: str | None = None


@dataclass(frozen=True)
class MarginLine:
    invoice_id: str
    connum: str
    normal_value: Decimal
    us_net_price: Decimal
    quantity: Decimal
    margin: Decimal
    dumping_amount: Decimal


@dataclass(frozen=True)
class MarginCalculationResult:
    matter_id: str
    weighted_average_margin: Decimal
    normal_values_by_connum: dict[str, Decimal]
    lines: list[MarginLine] = field(default_factory=list)


def to_jsonable(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    if hasattr(value, "__dataclass_fields__"):
        return to_jsonable(asdict(value))
    return value
