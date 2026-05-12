from datetime import date
from decimal import Decimal

from dumpingdesk_api.domain.models import CostOfProduction, ProceedingConfig, USSale
from dumpingdesk_api.domain.validation import validate_matter_data


def test_validation_flags_missing_cost_coverage_and_bad_costs():
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
            quantity=Decimal("5"),
            sale_date=date(2024, 2, 1),
        ),
        USSale(
            invoice_id="INV-2",
            connum="B200",
            gross_unit_price=Decimal("90"),
            quantity=Decimal("3"),
            sale_date=date(2025, 1, 1),
        ),
    ]
    costs = [CostOfProduction(connum="A100", variable_cost=Decimal("-1"), fixed_cost=Decimal("2"))]

    events = validate_matter_data(config, us_sales=us_sales, costs=costs)

    codes = {event.code for event in events}
    assert "MISSING_COST_COVERAGE" in codes
    assert "NON_POSITIVE_COST" in codes
    assert "SALE_DATE_OUTSIDE_PERIOD" in codes
    assert any(event.severity == "BLOCKING" for event in events)
