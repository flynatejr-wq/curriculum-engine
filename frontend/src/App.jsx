import { useState } from 'react'
import UploadForm from './components/UploadForm'
import StructureView from './components/StructureView'

export default function App() {
  const [state, setState] = useState({ status: 'idle', data: null, message: null })

  function handleResult(result) {
    if (result.status === 'uploading') {
      setState({ status: 'uploading', data: null, message: `Uploading ${result.file.name}…` })
    } else if (result.status === 'done') {
      setState({ status: 'done', data: result.data, message: null })
    } else {
      setState({ status: 'error', data: null, message: result.message })
    }
  }

  function reset() {
    setState({ status: 'idle', data: null, message: null })
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <div className="logo-mark" />
            <span className="logo-text">LessonGrove</span>
          </div>
        </div>
      </header>
      <main className="main">
        {state.status === 'idle' && (
          <div className="hero">
            <h1 className="hero-title">Analyse Your Textbook Structure</h1>
            <p className="hero-subtitle">Upload a PDF to detect its chapter and section breakdown before generating your curriculum.</p>
            <UploadForm onResult={handleResult} disabled={false} />
          </div>
        )}
        {state.status === 'uploading' && (
          <div className="hero hero--loading">
            <div className="spinner-large" />
            <p className="status-msg">Extracting text and detecting chapter structure…</p>
            <p className="status-note">This may take a moment for large textbooks.</p>
          </div>
        )}
        {state.status === 'error' && (
          <div className="hero hero--error">
            <p className="error-msg">❌ {state.message}</p>
            <button className="reset-btn" onClick={reset}>Try Again</button>
          </div>
        )}
        {state.status === 'done' && state.data && (
          <StructureView data={state.data} onReset={reset} />
        )}
      </main>
    </div>
  )
}
