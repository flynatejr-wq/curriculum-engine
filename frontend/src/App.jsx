import { useState } from 'react'
import UploadForm from './components/UploadForm'
import StructureView from './components/StructureView'
import CourseForm from './components/CourseForm'
import ScheduleView from './components/ScheduleView'

export default function App() {
  const [status, setStatus] = useState('idle')
  const [uploadData, setUploadData] = useState(null)
  const [scheduleData, setScheduleData] = useState(null)
  const [error, setError] = useState(null)

  function handleUploadResult(result) {
    if (result.status === 'uploading') {
      setStatus('uploading')
      setError(null)
    } else if (result.status === 'done') {
      setUploadData(result.data)
      setStatus('structure')
    } else {
      setError(result.message)
      setStatus('idle')
    }
  }

  async function handlePace(weeks, sessionsPerWeek) {
    setStatus('pacing')
    setError(null)
    try {
      const { paceCurriculum } = await import('./api.js')
      const data = await paceCurriculum(uploadData.session_id, weeks, sessionsPerWeek)
      setScheduleData(data)
      setStatus('schedule')
    } catch (err) {
      setError(err.message)
      setStatus('structure')
    }
  }

  function reset() {
    setStatus('idle')
    setUploadData(null)
    setScheduleData(null)
    setError(null)
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <div className="logo-mark" />
            <span className="logo-text">LessonGrove</span>
          </div>
          {status !== 'idle' && (
            <div className="breadcrumb">
              <span className={status === 'uploading' || status === 'structure' || status === 'pacing' || status === 'schedule' ? 'crumb crumb--active' : 'crumb'}>Structure</span>
              <span className="crumb-sep">›</span>
              <span className={status === 'schedule' || status === 'pacing' ? 'crumb crumb--active' : 'crumb'}>Schedule</span>
              <span className="crumb-sep">›</span>
              <span className="crumb">Lessons</span>
            </div>
          )}
        </div>
      </header>

      <main className="main">
        {status === 'idle' && (
          <div className="hero">
            <h1 className="hero-title">Turn any textbook into a full semester curriculum</h1>
            <p className="hero-subtitle">Upload a PDF — LessonGrove detects your book's structure, builds a paced schedule, and writes every lesson plan grounded in your actual text.</p>
            <UploadForm onResult={handleUploadResult} disabled={false} />
            {error && <p className="form-error">{error}</p>}
          </div>
        )}

        {status === 'uploading' && (
          <div className="hero hero--loading">
            <div className="spinner-large" />
            <p className="status-msg">Analysing textbook structure…</p>
            <p className="status-note">Extracting text and detecting chapters. May take a moment for large books.</p>
          </div>
        )}

        {status === 'structure' && uploadData && (
          <div className="two-col">
            <div className="two-col-main">
              <StructureView data={uploadData} onReset={reset} hideReset />
            </div>
            <div className="two-col-side">
              <CourseForm onSubmit={handlePace} disabled={false} />
              {error && <p className="form-error">{error}</p>}
            </div>
          </div>
        )}

        {status === 'pacing' && (
          <div className="hero hero--loading">
            <div className="spinner-large" />
            <p className="status-msg">Building schedule…</p>
          </div>
        )}

        {status === 'schedule' && scheduleData && (
          <ScheduleView data={scheduleData} onReset={reset} />
        )}
      </main>
    </div>
  )
}
