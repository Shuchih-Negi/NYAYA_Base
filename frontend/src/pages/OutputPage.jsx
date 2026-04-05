export default function OutputPage() {
  const stats = [
    ['18:42', 'SESSION DURATION'],
    ['7', 'EVENTS EXTRACTED'],
    ['86%', 'AVG CERTAINTY'],
    ['3', 'BNS SECTIONS'],
    ['~110 min', 'TIME SAVED'],
    ['SHA-256', 'TAMPER PROOF'],
  ]

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '1.25rem' }}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <section className="pdf-mockup">
          <h3>NYAYA LEGAL AID DOCUMENT</h3>
          <p>Prepared under BNS 2023 | Case: 2024-0047</p>
          <hr />
          <p>Structured testimony and Bayesian reconstruction are attached for counselor-reviewed legal drafting.</p>
        </section>
        <section className="panel scanlines" style={{ padding: '1rem' }}>
          <div className="stats-grid">
            {stats.map(([v, l]) => (
              <div key={l}>
                <div className="stat-value">{v}</div>
                <div className="mono-note">{l}</div>
              </div>
            ))}
          </div>
          <div className="sep" />
          <p className="closing-line a">Human-led.</p>
          <p className="closing-line b">AI-assisted.</p>
          <p className="closing-line c">Trauma-aware.</p>
          <button type="button" className="outline-btn">DOWNLOAD PDF</button>
        </section>
      </div>
    </div>
  )
}
