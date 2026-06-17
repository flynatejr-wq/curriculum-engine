import { useState, useEffect } from 'react'
import DropZone from './DropZone'

const STATUS_MESSAGES = ['Extracting text…', 'Chunking content…', 'Generating lessons…']

export default function UploadPanel({ status, onSubmit, error }) {
  const [file, setFile] = useState(null)
  const [title, setTitle] = useState('')
  const [msgIdx, setMsgIdx] = useState(0)

  useEffect(() => {
    if (status !== 'processing') return
    const id = setInterval(() => setMsgIdx(i => (i + 1) % STATUS_MESSAGES.length), 1500)
    return () => clearInterval(id)
  }, [status])

  if (status === 'results') return null

  const disabled = status === 'processing'
  const canSubmit = !!file && title.trim().length > 0 && status === 'idle'

  return (
    <div className="upload-panel">
      <div className="upload-hero">
        <h1 className="upload-title">Build Your Semester Curriculum</h1>
        <p className="upload-subtitle">Upload a textbook PDF and get a full 16-week lesson plan in seconds</p>
        <div className="upload-form">
          <DropZone file={file} onChange={setFile} disabled={disabled} />
          <input
            className="title-input"
            type="text"
            placeholder="Textbook title…"
            value={title}
            onChange={e => setTitle(e.target.value)}
            disabled={disabled}
          />
          <button
            className="generate-btn"
            disabled={!canSubmit}
            onClick={() => onSubmit(file, title)}
          >
            {disabled ? (
              <>
                <span className="spinner" />
                <span className="status-msg">{STATUS_MESSAGES[msgIdx]}</span>
              </>
            ) : 'Generate Curriculum ↗'}
          </button>
          {error && <p className="form-error">{error}</p>}
        </div>
      </div>
    </div>
  )
}
