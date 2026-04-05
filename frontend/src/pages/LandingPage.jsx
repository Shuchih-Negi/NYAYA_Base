import { Link } from 'react-router-dom'

export default function LandingPage() {
  return (
    <div
      style={{
        maxWidth: 960,
        margin: '0 auto',
        minHeight: 'calc(100vh - 2rem)',
        padding: '1rem 1.25rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <section
        style={{
          width: '100%',
          textAlign: 'center',
          padding: '3.5rem 1rem',
          border: '1px solid var(--border)',
          borderRadius: 4,
          background: 'linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.01))',
        }}
      >
        <p
          style={{
            margin: 0,
            fontFamily: 'JetBrains Mono, monospace',
            letterSpacing: '0.42em',
            fontSize: '0.66rem',
            color: 'var(--muted)',
            textTransform: 'uppercase',
          }}
        >
          Legal intelligence system
        </p>
        <h1
          style={{
            margin: '0.85rem 0 0.55rem',
            fontSize: 'clamp(3rem, 14vw, 8.25rem)',
            lineHeight: 0.92,
            fontWeight: 800,
            letterSpacing: '0.08em',
            color: '#ffffff',
            textShadow: '0 12px 30px rgba(255,255,255,0.14)',
          }}
        >
          NYAYA
        </h1>
        <p style={{ margin: '0 0 1.6rem', color: 'var(--dim)', fontSize: '0.95rem' }}>
          Human-led. AI-assisted.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
        <Link
          to="/consent"
          style={{
            padding: '0.75rem 1.5rem',
            borderRadius: 3,
            background: 'var(--accent)',
            color: 'var(--black)',
            fontWeight: 700,
            textDecoration: 'none',
            boxShadow: '0 8px 32px rgba(255, 255, 255, 0.2)',
          }}
        >
          Begin session
        </Link>
        <Link
          to="/interview"
          style={{
            padding: '0.75rem 1.5rem',
            borderRadius: 3,
            border: '1px solid var(--border)',
            color: 'var(--text)',
            textDecoration: 'none',
            fontWeight: 600,
          }}
        >
          Live monitor
        </Link>
        </div>
      </section>
    </div>
  )
}
