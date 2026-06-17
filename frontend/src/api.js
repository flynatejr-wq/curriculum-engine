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
