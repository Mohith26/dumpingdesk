export type PipelineStage = {
  stage: string;
  status: string;
  blocking_events?: number;
};

export type MatterSummary = {
  matter: {
    matter_id: string;
    case_number: string;
    period_start: string;
    period_end: string;
    proceeding_type: string;
    segment: string;
    methodology_version: string;
  };
  pipeline: PipelineStage[];
  calculation: {
    weighted_average_margin: string;
    normal_values_by_connum: Record<string, string>;
    lines: Array<{
      invoice_id: string;
      connum: string;
      normal_value: string;
      us_net_price: string;
      quantity: string;
      margin: string;
      dumping_amount: string;
    }>;
  };
};

export type ReviewItem = {
  id: string;
  type: string;
  status: string;
  title: string;
  severity: "INFO" | "WARNING" | "ERROR" | "BLOCKING";
  message: string;
};

const fallbackMatter: MatterSummary = {
  matter: {
    matter_id: "demo-matter",
    case_number: "A-570-123",
    period_start: "2024-01-01",
    period_end: "2024-12-31",
    proceeding_type: "AD",
    segment: "admin_review",
    methodology_version: "2024.3",
  },
  pipeline: [
    { stage: "ingestion", status: "complete" },
    { stage: "validation", status: "needs_review", blocking_events: 1 },
    { stage: "calculation", status: "complete" },
    { stage: "drafting", status: "not_started" },
    { stage: "output", status: "not_started" },
  ],
  calculation: {
    weighted_average_margin: "0.315385",
    normal_values_by_connum: { A100: "114.000000", B200: "82.000000" },
    lines: [
      {
        invoice_id: "INV-1001",
        connum: "A100",
        normal_value: "114.000000",
        us_net_price: "90",
        quantity: "10",
        margin: "0.266667",
        dumping_amount: "240.000000",
      },
      {
        invoice_id: "INV-1002",
        connum: "A100",
        normal_value: "114.000000",
        us_net_price: "80",
        quantity: "5",
        margin: "0.425000",
        dumping_amount: "170.000000",
      },
    ],
  },
};

const fallbackReviewItems: ReviewItem[] = [
  {
    id: "validation-1",
    type: "validation_event",
    status: "open",
    title: "Missing Cost Coverage",
    severity: "BLOCKING",
    message: "U.S.-sold CONNUM B200 has no cost record.",
  },
  {
    id: "draft-section-c",
    type: "ai_draft",
    status: "not_started",
    title: "Section C narrative draft",
    severity: "INFO",
    message: "Drafting is scaffolded for the next implementation phase.",
  },
];

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function getMatterSummary(): Promise<MatterSummary> {
  try {
    const response = await fetch(`${apiBaseUrl}/api/v1/matters/demo`, {
      cache: "no-store",
    });
    if (!response.ok) {
      return fallbackMatter;
    }
    return (await response.json()) as MatterSummary;
  } catch {
    return fallbackMatter;
  }
}

export async function getReviewQueue(): Promise<ReviewItem[]> {
  try {
    const response = await fetch(`${apiBaseUrl}/api/v1/matters/demo/review-queue`, {
      cache: "no-store",
    });
    if (!response.ok) {
      return fallbackReviewItems;
    }
    return (await response.json()) as ReviewItem[];
  } catch {
    return fallbackReviewItems;
  }
}
