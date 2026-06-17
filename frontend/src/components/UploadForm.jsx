import { useRef, useState } from 'react'

export default function UploadForm({ onResult, disabled }) {
  const [dragging, setDragging] = useState(false)
  const [file, setFile] = useState(null)
  const inputRef = useRef(null)

  function handleDrop(e) {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files[0]
    if (f?.name.toLowerCase().endsWith('.pdf')) setFile(f)
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!file) return
    onResult({ status: 'uploading', file })
    try {
      const { uploadPDF } = await import('../api.js')
      const data = await uploadPDF(file)
      onResult({ status: 'done', data })
    } catch (err) {
      onResult({ status: 'error', message: err.message })
    }
  }

  return (
    <form className="upload-form" onSubmit={handleSubmit}>
      <div
        className={['dropzone', dragging && 'dropzone--active', file && 'dropzone--filled'].filter(Boolean).join(' ')}
        onClick={() => !disabled && !file && inputRef.current.click()}
        onDragOver={e => { e.preventDefault(); if (!disabled) setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
      >
        {file ? (
          <div className="dropzone-prompt">
            <span className="dropzone-filename">📄 {file.name}</span>
            <button
              type="button"
              className="dropzone-clear"
              onClick={e => { e.stopPropagation(); setFile(null) }}
            >✕</button>
          </div>
        ) : (
          <div className="dropzone-prompt">
            <span className="dropzone-icon">📄</span>
            <span className="dropzone-hint">Drop your textbook PDF here or click to browse</span>
          </div>
        )}
        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          style={{ display: 'none' }}
          onChange={e => { if (e.target.files[0]) setFile(e.target.files[0]) }}
        />
      </div>
      <button className="submit-btn" type="submit" disabled={!file || disabled}>
        Analyse Structure ↗
      </button>
    </form>
  )
}
