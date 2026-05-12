from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dumpingdesk_api.domain.calculations import calculate_ad_margin
from dumpingdesk_api.domain.models import to_jsonable
from dumpingdesk_api.domain.validation import validate_matter_data
from dumpingdesk_api.sample_data import (
    sample_config,
    sample_costs,
    sample_home_market_sales,
    sample_us_sales,
)

app = FastAPI(title="DumpingDesk API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "dumpingdesk-api"}


@app.get("/api/v1/matters/demo")
def get_demo_matter() -> dict[str, object]:
    config = sample_config()
    events = validate_matter_data(config, us_sales=sample_us_sales(), costs=sample_costs())
    calculation = calculate_ad_margin(config, sample_us_sales(), sample_home_market_sales())
    return to_jsonable(
        {
            "matter": config,
            "pipeline": [
                {"stage": "ingestion", "status": "complete"},
                {
                    "stage": "validation",
                    "status": "needs_review" if events else "complete",
                    "blocking_events": len([event for event in events if event.severity == "BLOCKING"]),
                },
                {"stage": "calculation", "status": "complete"},
                {"stage": "drafting", "status": "not_started"},
                {"stage": "output", "status": "not_started"},
            ],
            "calculation": calculation,
        }
    )


@app.get("/api/v1/matters/demo/validation/events")
def get_demo_validation_events() -> list[dict[str, object]]:
    config = sample_config()
    events = validate_matter_data(config, us_sales=sample_us_sales(), costs=sample_costs())
    return to_jsonable(events)


@app.post("/api/v1/matters/demo/calculate/ad-margin")
def run_demo_ad_margin() -> dict[str, object]:
    config = sample_config()
    result = calculate_ad_margin(config, sample_us_sales(), sample_home_market_sales())
    return to_jsonable(result)


@app.get("/api/v1/matters/demo/review-queue")
def get_demo_review_queue() -> list[dict[str, object]]:
    config = sample_config()
    events = validate_matter_data(config, us_sales=sample_us_sales(), costs=sample_costs())
    review_items = [
        {
            "id": f"validation-{index}",
            "type": "validation_event",
            "status": "open",
            "title": event.code.replace("_", " ").title(),
            "severity": event.severity,
            "message": event.message,
        }
        for index, event in enumerate(events, start=1)
    ]
    review_items.append(
        {
            "id": "draft-section-c",
            "type": "ai_draft",
            "status": "not_started",
            "title": "Section C narrative draft",
            "severity": "INFO",
            "message": "Drafting is scaffolded for the next implementation phase.",
        }
    )
    return review_items
