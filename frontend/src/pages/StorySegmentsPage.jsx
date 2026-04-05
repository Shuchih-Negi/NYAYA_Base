import { useMemo } from 'react'
import { computeBayesianTemporalInference, DUMMY_STORY_SEGMENTS } from '../modules/bayesianTemporalDummy.js'

export default function StorySegmentsPage() {
  const result = useMemo(() => computeBayesianTemporalInference(DUMMY_STORY_SEGMENTS), [])

  return (
    <div style={{ maxWidth: 1080, margin: '0 auto', padding: '1.25rem' }}>
      <header style={{ marginBottom: '1rem' }}>
        <h1 style={{ margin: 0, fontSize: '1.25rem' }}>Story Segments - Bayesian Temporal Inference</h1>
        <p style={{ margin: '0.4rem 0 0', color: 'var(--dim)', fontSize: '0.9rem' }}>
          Dummy testimony split into segments, then ranked with pairwise Bayesian temporal probabilities.
        </p>
      </header>

      <section className="panel scanlines" style={{ padding: '1rem', marginBottom: '1rem' }}>
        <h2 className="panel-title">Original Segments</h2>
        <div style={{ display: 'grid', gap: '0.55rem' }}>
          {result.segments.map((s, idx) => (
            <article key={s.id} style={{ border: '1px solid var(--border)', borderRadius: 2, padding: '0.65rem 0.75rem' }}>
              <div style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: 11, color: 'var(--dim)' }}>
                {idx + 1}. {s.id}
              </div>
              <div style={{ fontSize: 14 }}>{s.text}</div>
            </article>
          ))}
        </div>
      </section>

      <section className="panel scanlines" style={{ padding: '1rem', marginBottom: '1rem' }}>
        <h2 className="panel-title">Inferred Chronological Order</h2>
        <ol style={{ margin: 0, paddingLeft: '1.15rem' }}>
          {result.ordered.map((s) => (
            <li key={s.id} style={{ marginBottom: '0.75rem' }}>
              <strong style={{ color: '#ffffff' }}>
                #{s.rank} {s.id}
              </strong>{' '}
              <span style={{ color: 'var(--dim)', fontFamily: 'JetBrains Mono, monospace', fontSize: 12 }}>
                P={s.probability.toFixed(3)}
              </span>
              <div style={{ fontSize: 14, marginTop: 4 }}>{s.text}</div>
            </li>
          ))}
        </ol>
      </section>

      <section className="panel scanlines" style={{ padding: '1rem' }}>
        <h2 className="panel-title">Pairwise Matrix (P[i before j])</h2>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
            <thead>
              <tr>
                <th style={thStyle}>i \ j</th>
                {result.segments.map((s) => (
                  <th key={s.id} style={thStyle}>{s.id}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {result.pairwise.map((row, i) => (
                <tr key={result.segments[i].id}>
                  <td style={tdHeadStyle}>{result.segments[i].id}</td>
                  {row.map((v, j) => (
                    <td key={`${i}-${j}`} style={tdStyle}>{v.toFixed(2)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

const thStyle = {
  border: '1px solid var(--border)',
  padding: '0.4rem 0.5rem',
  color: 'var(--dim)',
  fontFamily: 'JetBrains Mono, monospace',
  fontWeight: 600,
}

const tdStyle = {
  border: '1px solid var(--border)',
  padding: '0.38rem 0.45rem',
  textAlign: 'center',
  color: 'var(--text)',
}

const tdHeadStyle = {
  ...tdStyle,
  textAlign: 'left',
  fontFamily: 'JetBrains Mono, monospace',
  color: 'var(--dim)',
}
