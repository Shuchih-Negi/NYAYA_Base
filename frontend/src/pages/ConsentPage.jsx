import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function ConsentPage() {
  const [ok, setOk] = useState(false)
  const [busy, setBusy] = useState(false)
  const navigate = useNavigate()

  const begin = async () => {
    if (!ok || busy) return
    setBusy(true)
    try {
      await navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    } catch {
      // fallback for demo environments
    } finally {
      setBusy(false)
      navigate('/interview')
    }
  }

  return (
    <div className="consent-wrap">
      <section className="consent-card scanlines">
        <p className="eyebrow">INFORMED CONSENT - CASE INTAKE</p>
        <h1 className="consent-title">Before we begin</h1>
        <div className="consent-divider" />
        <p className="consent-copy">
          This session will use your camera and microphone to capture your testimony. All processing happens on this
          device. Nothing is transmitted to any server without your explicit action. You may stop at any time.
        </p>
        <ul className="consent-list">
          <li>Camera access - used for facial landmark analysis only. No video is stored.</li>
          <li>Microphone access - speech is transcribed locally via Whisper-compatible API.</li>
          <li>On-device processing - facial data exists for 15 seconds only, then discarded.</li>
          <li>Right to erasure - all session data deleted within 7 days on request.</li>
        </ul>
        <label className="consent-check-row">
          <input type="checkbox" checked={ok} onChange={(e) => setOk(e.target.checked)} />
          <span>I understand and consent to the above. I am proceeding voluntarily.</span>
        </label>
        <button type="button" disabled={!ok || busy} className="cta" onClick={begin}>
          {busy ? 'REQUESTING PERMISSIONS...' : 'BEGIN SESSION - ACTIVATE CAMERA & MICROPHONE'}
        </button>
      </section>
    </div>
  )
}
