const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function uploadPDF(file) {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${BASE_URL}/upload`, { method: 'POST', body: form })
  if (!res.ok) {
    let msg
    try {
      const body = await res.json()
      msg = body.detail || JSON.stringify(body)
    } catch {
      msg = await res.text()
    }
    throw new Error(msg || `Upload failed (${res.status})`)
  }
  return res.json()
}

export async function paceCurriculum(sessionId, totalWeeks, sessionsPerWeek) {
  const res = await fetch(`${BASE_URL}/pace`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      total_weeks: totalWeeks,
      sessions_per_week: sessionsPerWeek,
    }),
  })
  if (!res.ok) {
    let msg
    try { const b = await res.json(); msg = b.detail || JSON.stringify(b) }
    catch { msg = await res.text() }
    throw new Error(msg || `Pace failed (${res.status})`)
  }
  return res.json()
}
