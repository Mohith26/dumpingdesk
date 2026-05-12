from __future__ import annotations

from datetime import date
from decimal import Decimal

from dumpingdesk_api.domain.models import CostOfProduction, HomeMarketSale, ProceedingConfig, USSale


def sample_config() -> ProceedingConfig:
    return ProceedingConfig(
        matter_id="demo-matter",
        case_number="A-570-123",
        period_start=date(2024, 1, 1),
        period_end=date(2024, 12, 31),
    )


def sample_us_sales() -> list[USSale]:
    return [
        USSale(
            invoice_id="INV-1001",
            connum="A100",
            gross_unit_price=Decimal("100"),
            quantity=Decimal("10"),
            sale_date=date(2024, 2, 1),
            movement_expense=Decimal("10"),
        ),
        USSale(
            invoice_id="INV-1002",
            connum="A100",
            gross_unit_price=Decimal("80"),
            quantity=Decimal("5"),
            sale_date=date(2024, 2, 5),
        ),
        USSale(
            invoice_id="INV-1003",
            connum="B200",
            gross_unit_price=Decimal("75"),
            quantity=Decimal("4"),
            sale_date=date(2024, 3, 3),
        ),
    ]


def sample_home_market_sales() -> list[HomeMarketSale]:
    return [
        HomeMarketSale(
            invoice_id="HM-2001",
            connum="A100",
            gross_unit_price=Decimal("110"),
            quantity=Decimal("6"),
            sale_date=date(2024, 2, 2),
        ),
        HomeMarketSale(
            invoice_id="HM-2002",
            connum="A100",
            gross_unit_price=Decimal("120"),
            quantity=Decimal("4"),
            sale_date=date(2024, 2, 4),
        ),
        HomeMarketSale(
            invoice_id="HM-2003",
            connum="B200",
            gross_unit_price=Decimal("82"),
            quantity=Decimal("4"),
            sale_date=date(2024, 3, 6),
        ),
    ]


def sample_costs() -> list[CostOfProduction]:
    return [
        CostOfProduction(connum="A100", variable_cost=Decimal("62"), fixed_cost=Decimal("14")),
    ]
