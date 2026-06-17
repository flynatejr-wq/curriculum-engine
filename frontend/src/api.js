const BASE_URL = 'http://localhost:8000'

export async function uploadTextbook(file, title) {
  const form = new FormData()
  form.append('file', file)
  form.append('title', title)
  const res = await fetch(`${BASE_URL}/upload`, { method: 'POST', body: form })
  if (!res.ok) {
    if (res.status === 422) throw new Error('This PDF has no extractable text. Try a different file.')
    const text = await res.text()
    throw new Error(text || `Upload failed (${res.status})`)
  }
  return res.json()
}
