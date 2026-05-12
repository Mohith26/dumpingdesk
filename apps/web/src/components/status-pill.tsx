type StatusPillProps = {
  status: string;
};

export function StatusPill({ status }: StatusPillProps) {
  const label = status.replaceAll("_", " ");
  return <span className={`status-pill status-${status}`}>{label}</span>;
}
