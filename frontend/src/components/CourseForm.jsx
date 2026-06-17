import { useState } from 'react'

export default function CourseForm({ onSubmit, disabled }) {
  const [weeks, setWeeks] = useState(16)
  const [sessionsPerWeek, setSessionsPerWeek] = useState(3)

  const totalSessions = weeks * sessionsPerWeek

  function handleSubmit(e) {
    e.preventDefault()
    onSubmit(weeks, sessionsPerWeek)
  }

  return (
    <form className="course-form" onSubmit={handleSubmit}>
      <h2 className="course-form-title">Set your course length</h2>
      <p className="course-form-subtitle">
        LessonGrove will build a {totalSessions}-session schedule that respects your textbook's chapter structure.
      </p>
      <div className="course-fields">
        <label className="course-field">
          <span className="course-label">Total weeks</span>
          <input
            type="number"
            className="course-input"
            min={1}
            max={52}
            value={weeks}
            onChange={e => setWeeks(Number(e.target.value))}
            disabled={disabled}
          />
        </label>
        <span className="course-times">×</span>
        <label className="course-field">
          <span className="course-label">Sessions per week</span>
          <input
            type="number"
            className="course-input"
            min={1}
            max={7}
            value={sessionsPerWeek}
            onChange={e => setSessionsPerWeek(Number(e.target.value))}
            disabled={disabled}
          />
        </label>
        <span className="course-equals">= {totalSessions} sessions</span>
      </div>
      <button className="submit-btn" type="submit" disabled={disabled}>
        Build Schedule ↗
      </button>
    </form>
  )
}
