import { useState } from 'react'
import UploadForm from './components/UploadForm'
import StructureView from './components/StructureView'
import CourseForm from './components/CourseForm'
import ScheduleView from './components/ScheduleView'
import LessonView from './components/LessonView'

export default function App() {
  const [status, setStatus] = useState('idle')
  const [uploadData, setUploadData] = useState(null)
  const [scheduleData, setScheduleData] = useState(null)
  const [lessons, setLessons] = useState({})          // session_number → LessonPlan
  const [isGenerating, setIsGenerating] = useState(false)
  const [genProgress, setGenProgress] = useState(null) // { current, total }
  const [activeLesson, setActiveLesson] = useState(null)
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
      setLessons({})
      setGenProgress(null)
      setStatus('schedule')
    } catch (err) {
      setError(err.message)
      setStatus('structure')
    }
  }

  async function handleGenerateLessons() {
    if (!scheduleData || isGenerating) return
    setIsGenerating(true)
    setError(null)
    const total = scheduleData.schedule.total_sessions
    setGenProgress({ current: 0, total })

    try {
      const { generateLessons } = await import('./api.js')
      await generateLessons(uploadData.session_id, (event) => {
        if (event.status === 'generating') {
          setGenProgress({ current: event.session_number, total: event.total_sessions })
        } else if (event.status === 'done' && event.lesson) {
          setLessons(prev => ({ ...prev, [event.lesson.session_number]: event.lesson }))
          setGenProgress({ current: event.session_number, total: event.total_sessions })
        } else if (event.status === 'error') {
          console.warn(`Lesson ${event.session_number} error:`, event.error)
        }
      })
    } catch (err) {
      setError(err.message)
    } finally {
      setIsGenerating(false)
      setGenProgress(null)
    }
  }

  function handleViewLesson(lesson) {
    setActiveLesson(lesson)
    setStatus('lesson')
  }

  function handleBackToSchedule() {
    setActiveLesson(null)
    setStatus('schedule')
  }

  function reset() {
    setStatus('idle')
    setUploadData(null)
    setScheduleData(null)
    setLessons({})
    setIsGenerating(false)
    setGenProgress(null)
    setActiveLesson(null)
    setError(null)
  }

  const breadcrumbVisible = status !== 'idle'

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <svg className="logo-mark" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path d="M15 3C15 3 24 8 24 16C24 22.5 20 27 15 28C10 27 6 22.5 6 16C6 8 15 3 15 3Z" fill="#1d4a2e"/>
              <line x1="15" y1="8" x2="15" y2="26" stroke="#7aaf8a" strokeWidth="1.2" strokeLinecap="round"/>
              <path d="M15 12C17.5 9.5 21 9 21 9" stroke="#7aaf8a" strokeWidth="0.9" strokeLinecap="round"/>
              <path d="M15 16C17.5 13.5 22 12.5 22 12.5" stroke="#7aaf8a" strokeWidth="0.9" strokeLinecap="round"/>
              <path d="M15 12C12.5 9.5 9 9 9 9" stroke="#7aaf8a" strokeWidth="0.9" strokeLinecap="round"/>
              <path d="M15 16C12.5 13.5 8 12.5 8 12.5" stroke="#7aaf8a" strokeWidth="0.9" strokeLinecap="round"/>
            </svg>
            <span className="logo-text">LessonGrove</span>
          </div>
          {breadcrumbVisible && (
            <div className="breadcrumb">
              <span className={['uploading', 'structure', 'pacing', 'schedule', 'lesson'].includes(status) ? 'crumb crumb--active' : 'crumb'}>Structure</span>
              <span className="crumb-sep">›</span>
              <span className={['schedule', 'lesson'].includes(status) ? 'crumb crumb--active' : 'crumb'}>Schedule</span>
              <span className="crumb-sep">›</span>
              <span className={status === 'lesson' ? 'crumb crumb--active' : 'crumb'}>Lessons</span>
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
          <>
            <ScheduleView
              data={scheduleData}
              lessons={lessons}
              isGenerating={isGenerating}
              genProgress={genProgress}
              onGenerateLessons={handleGenerateLessons}
              onViewLesson={handleViewLesson}
              onReset={reset}
            />
            {error && <p className="form-error" style={{ textAlign: 'center', marginTop: '1rem' }}>{error}</p>}
          </>
        )}

        {status === 'lesson' && activeLesson && (
          <LessonView lesson={activeLesson} onBack={handleBackToSchedule} />
        )}
      </main>
    </div>
  )
}
