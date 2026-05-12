import type { ReviewItem } from "@/lib/api";

type SeverityBadgeProps = {
  severity: ReviewItem["severity"];
};

export function SeverityBadge({ severity }: SeverityBadgeProps) {
  return <span className={`severity-badge severity-${severity}`}>{severity}</span>;
}
