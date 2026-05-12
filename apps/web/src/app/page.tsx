import { SeverityBadge } from "@/components/severity-badge";
import { StatusPill } from "@/components/status-pill";
import { getMatterSummary, getReviewQueue } from "@/lib/api";

export default async function Home() {
  const [summary, reviewQueue] = await Promise.all([getMatterSummary(), getReviewQueue()]);
  const blockingCount = reviewQueue.filter((item) => item.severity === "BLOCKING").length;

  return (
    <main className="page-shell">
      <section className="hero-panel" aria-labelledby="page-title">
        <div>
          <p className="eyebrow">DumpingDesk MVP</p>
          <h1 id="page-title">Administrative review workspace</h1>
          <p className="hero-copy">
            Flat-file ingestion, validation, margin calculation, and attorney review are wired
            into one focused demo matter.
          </p>
        </div>
        <div className="matter-card" aria-label="Matter details">
          <span>{summary.matter.case_number}</span>
          <strong>{summary.matter.proceeding_type}</strong>
          <small>
            POR {summary.matter.period_start} to {summary.matter.period_end}
          </small>
        </div>
      </section>

      <section className="metrics-grid" aria-label="Matter metrics">
        <article className="metric-card">
          <span>Weighted-average margin</span>
          <strong>{formatPercent(summary.calculation.weighted_average_margin)}</strong>
          <small>Decimal arithmetic, value weighted</small>
        </article>
        <article className="metric-card">
          <span>CONNUMs with NV</span>
          <strong>{Object.keys(summary.calculation.normal_values_by_connum).length}</strong>
          <small>Home-market comparison pool</small>
        </article>
        <article className="metric-card">
          <span>Review blockers</span>
          <strong>{blockingCount}</strong>
          <small>Must clear before output</small>
        </article>
      </section>

      <section className="content-grid">
        <article className="panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Pipeline</p>
              <h2>Workflow status</h2>
            </div>
          </div>
          <ol className="pipeline-list">
            {summary.pipeline.map((stage) => (
              <li key={stage.stage}>
                <span>{stage.stage.replaceAll("_", " ")}</span>
                <StatusPill status={stage.status} />
              </li>
            ))}
          </ol>
        </article>

        <article className="panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Attorney queue</p>
              <h2>Open review items</h2>
            </div>
          </div>
          <div className="review-list">
            {reviewQueue.map((item) => (
              <div className="review-item" key={item.id}>
                <div>
                  <h3>{item.title}</h3>
                  <p>{item.message}</p>
                </div>
                <SeverityBadge severity={item.severity} />
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">Calculation detail</p>
            <h2>Transaction margin preview</h2>
          </div>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Invoice</th>
                <th>CONNUM</th>
                <th>Normal value</th>
                <th>U.S. net price</th>
                <th>Quantity</th>
                <th>Margin</th>
              </tr>
            </thead>
            <tbody>
              {summary.calculation.lines.map((line) => (
                <tr key={line.invoice_id}>
                  <td>{line.invoice_id}</td>
                  <td>{line.connum}</td>
                  <td>{line.normal_value}</td>
                  <td>{line.us_net_price}</td>
                  <td>{line.quantity}</td>
                  <td>{formatPercent(line.margin)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}

function formatPercent(value: string) {
  return `${(Number(value) * 100).toFixed(2)}%`;
}
