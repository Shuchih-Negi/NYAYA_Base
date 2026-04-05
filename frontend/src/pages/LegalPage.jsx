import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import * as api from '../api.js'
import { useCase } from '../context/CaseContext.jsx'

export default function LegalPage() {
  const { caseId, caseData, refreshCase, ensure } = useCase()
  const [bnsSuggestions, setBnsSuggestions] = useState([])
  const [selectedBns, setSelectedBns] = useState([])
  const [busy, setBusy] = useState('')
  const [lastFingerprint, setLastFingerprint] = useState('')

  useEffect(() => {
    ensure().then(() => refreshCase())
  }, [ensure, refreshCase])

  useEffect(() => {
    if (Array.isArray(caseData?.verified_bns)) setSelectedBns(caseData.verified_bns)
  }, [caseData])

  const suggestBns = useCallback(async () => {
    setBusy('BNS semantic search…')
    try {
      const s = await api.bnsSuggest(caseId)
      setBnsSuggestions(s.suggestions || [])
    } finally {
      setBusy('')
    }
  }, [caseId])

  const toggleBns = async (id) => {
    const next = selectedBns.includes(id) ? selectedBns.filter((x) => x !== id) : [...selectedBns, id]
    setSelectedBns(next)
    await api.verifyBns(caseId, next)
  }

  const genPdf = async () => {
    if (!selectedBns.length) {
      alert('Select at least one BNS section.')
      return
    }
    setBusy('Compiling legal aid PDF…')
    try {
      await api.verifyBns(caseId, selectedBns)
      const { blob, fingerprint } = await api.downloadPdf(caseId)
      setLastFingerprint(fingerprint)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `nyaya-${caseId}.pdf`
      a.click()
      URL.revokeObjectURL(url)
      await refreshCase()
    } catch (e) {
      alert(e.message || String(e))
    } finally {
      setBusy('')
    }
  }

  return (
    <div style={{ maxWidth: 720, margin: '0 auto', padding: '1.25rem' }}>
      <header style={{ marginBottom: '1.25rem' }}>
        <h1 style={{ margin: 0, fontSize: '1.35rem' }}>BNS mapping · legal aid PDF</h1>
        <p style={{ margin: '0.35rem 0 0', color: 'var(--muted)', fontSize: '0.88rem' }}>
          Counselor verifies sections — PDF bundles testimony + pitch timeline + Bayesian cues + fingerprint.{' '}
          <Link to="/output" style={{ color: 'var(--accent)' }}>
            Case output →
          </Link>
        </p>
        {busy && <p style={{ color: 'var(--accent)', fontSize: '0.85rem' }}>{busy}</p>}
      </header>

      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
        <button
          type="button"
          onClick={suggestBns}
          style={{
            padding: '0.45rem 0.9rem',
            borderRadius: 3,
            border: '1px solid var(--border)',
            background: '#0f0f0f',
            color: 'var(--text)',
          }}
        >
          Suggest BNS (FAISS)
        </button>
      </div>

      <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 1rem' }}>
        {(bnsSuggestions || []).map((s) => (
          <li
            key={s.id}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.65rem',
              marginBottom: '0.5rem',
              fontSize: '0.9rem',
              padding: '0.5rem 0.75rem',
              borderRadius: 3,
              background: 'var(--panel)',
              border: '1px solid var(--border)',
            }}
          >
            <input
              type="checkbox"
              checked={selectedBns.includes(s.id)}
              onChange={() => toggleBns(s.id)}
              id={`bns-${s.id}`}
            />
            <label htmlFor={`bns-${s.id}`} style={{ cursor: 'pointer', flex: 1 }}>
              {s.id} — {s.title}{' '}
              <span style={{ color: 'var(--muted)', fontSize: '0.75rem' }}>[{s.confidence}]</span>
            </label>
          </li>
        ))}
      </ul>

      {bnsSuggestions.length === 0 && (
        <p style={{ color: 'var(--muted)', fontSize: '0.85rem' }}>Run suggest after you have transcript data on the server.</p>
      )}

      <button
        type="button"
        onClick={genPdf}
        disabled={!selectedBns.length}
        style={{
          padding: '0.75rem 1.5rem',
          borderRadius: 3,
          border: 'none',
          fontWeight: 700,
          background: selectedBns.length ? 'var(--accent)' : '#2b2b2b',
          color: selectedBns.length ? 'var(--black)' : '#fff',
          boxShadow: selectedBns.length ? '0 10px 36px rgba(255, 255, 255, 0.2)' : 'none',
        }}
      >
        Generate legal aid PDF
      </button>

      {caseData?.pdf_hash && (
        <p style={{ margin: '1rem 0 0', fontSize: '0.75rem', color: 'var(--muted)', wordBreak: 'break-all' }}>
          Stored fingerprint: {caseData.pdf_hash}
        </p>
      )}
      {lastFingerprint && (
        <p style={{ margin: '0.35rem 0 0', fontSize: '0.75rem', color: 'var(--muted)', wordBreak: 'break-all' }}>
          Last download: {lastFingerprint}
        </p>
      )}
    </div>
  )
}
