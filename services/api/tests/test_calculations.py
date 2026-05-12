from datetime import date
from decimal import Decimal

from dumpingdesk_api.domain.calculations import calculate_ad_margin
from dumpingdesk_api.domain.models import HomeMarketSale, ProceedingConfig, USSale


def test_calculates_weighted_average_ad_margin_with_decimal_arithmetic():
    config = ProceedingConfig(
        matter_id="matter-1",
        case_number="A-570-123",
        period_start=date(2024, 1, 1),
        period_end=date(2024, 12, 31),
    )
    us_sales = [
        USSale(
            invoice_id="INV-1",
            connum="A100",
            gross_unit_price=Decimal("100"),
            quantity=Decimal("10"),
            sale_date=date(2024, 2, 1),
            movement_expense=Decimal("10"),
        ),
        USSale(
            invoice_id="INV-2",
            connum="A100",
            gross_unit_price=Decimal("80"),
            quantity=Decimal("5"),
            sale_date=date(2024, 2, 5),
        ),
    ]
    home_market_sales = [
        HomeMarketSale(
            invoice_id="HM-1",
            connum="A100",
            gross_unit_price=Decimal("110"),
            quantity=Decimal("6"),
            sale_date=date(2024, 2, 2),
        ),
        HomeMarketSale(
            invoice_id="HM-2",
            connum="A100",
            gross_unit_price=Decimal("120"),
            quantity=Decimal("4"),
            sale_date=date(2024, 2, 4),
        ),
    ]

    result = calculate_ad_margin(config, us_sales, home_market_sales)

    assert result.normal_values_by_connum["A100"] == Decimal("114.000000")
    assert result.weighted_average_margin == Decimal("0.315385")
    assert [line.margin for line in result.lines] == [Decimal("0.266667"), Decimal("0.425000")]
