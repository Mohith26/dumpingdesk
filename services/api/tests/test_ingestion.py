from decimal import Decimal

from dumpingdesk_api.domain.ingestion import FieldMapping, ingest_tabular_file
from dumpingdesk_api.domain.models import DatasetKind


def test_ingests_us_sales_csv_into_canonical_records(tmp_path):
    source = tmp_path / "us_sales.csv"
    source.write_text(
        "\n".join(
            [
                "invoice,connum,price,qty,date,currency,freight",
                "INV-1,A100,125.50,10,2024-02-15,USD,5.50",
            ]
        ),
        encoding="utf-8",
    )

    records = ingest_tabular_file(
        source,
        DatasetKind.US_SALES,
        FieldMapping(
            {
                "invoice_id": "invoice",
                "connum": "connum",
                "gross_unit_price": "price",
                "quantity": "qty",
                "sale_date": "date",
                "currency": "currency",
                "movement_expense": "freight",
            }
        ),
    )

    assert len(records) == 1
    sale = records[0]
    assert sale.invoice_id == "INV-1"
    assert sale.connum == "A100"
    assert sale.gross_unit_price == Decimal("125.50")
    assert sale.quantity == Decimal("10")
    assert sale.net_unit_price == Decimal("120.00")
