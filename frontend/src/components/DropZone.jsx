import { useRef, useState } from 'react'

export default function DropZone({ file, onChange, disabled }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)

  function handleDragOver(e) {
    e.preventDefault()
    if (!disabled) setDragging(true)
  }

  function handleDragLeave() {
    setDragging(false)
  }

  function handleDrop(e) {
    e.preventDefault()
    setDragging(false)
    if (!disabled && e.dataTransfer.files[0]) onChange(e.dataTransfer.files[0])
  }

  function handleClick() {
    if (!disabled && !file) inputRef.current.click()
  }

  function handleInputChange(e) {
    if (e.target.files[0]) onChange(e.target.files[0])
  }

  const cls = ['dropzone', dragging && 'dropzone--active', file && 'dropzone--filled']
    .filter(Boolean).join(' ')

  return (
    <div className={cls} onClick={handleClick} onDragOver={handleDragOver}
         onDragLeave={handleDragLeave} onDrop={handleDrop}>
      {file ? (
        <div className="dropzone-prompt">
          <span className="dropzone-filename">{file.name}</span>
          <button className="dropzone-clear" onClick={e => { e.stopPropagation(); onChange(null) }}>✕</button>
        </div>
      ) : (
        <div className="dropzone-prompt">
          <span className="dropzone-icon">📄</span>
          <span className="dropzone-hint">Drop your PDF here or click to browse</span>
        </div>
      )}
      <input ref={inputRef} type="file" accept=".pdf" style={{ display: 'none' }}
             onChange={handleInputChange} />
    </div>
  )
}
