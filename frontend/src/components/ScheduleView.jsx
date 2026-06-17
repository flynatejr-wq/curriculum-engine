import { useState } from 'react'

export default function ScheduleView({ data, onReset }) {
  const { filename, schedule } = data
  const { total_weeks, sessions_per_week, total_sessions, target_pages_per_session, sessions } = schedule

  // Group sessions by week
  const byWeek = sessions.reduce((acc, s) => {
    if (!acc[s.week_number]) acc[s.week_number] = []
    acc[s.week_number].push(s)
    return acc
  }, {})
  const weeks = Object.keys(byWeek).map(Number).sort((a, b) => a - b)

  const [openWeeks, setOpenWeeks] = useState(new Set([1]))

  function toggleWeek(w) {
    setOpenWeeks(prev => {
      const next = new Set(prev)
      next.has(w) ? next.delete(w) : next.add(w)
      return next
    })
  }

  return (
    <div className="schedule-view">
      <div className="schedule-header">
        <h2 className="schedule-title">{filename}</h2>
        <p className="schedule-meta">
          {total_weeks} weeks · {sessions_per_week} sessions/week · {total_sessions} sessions · ~{target_pages_per_session} pages/session
        </p>
      </div>

      <div className="schedule-weeks">
        {weeks.map(w => {
          const isOpen = openWeeks.has(w)
          const weekSessions = byWeek[w]
          return (
            <div key={w} className={`week-block${isOpen ? ' week-block--open' : ''}`}>
              <div className="week-block-header" onClick={() => toggleWeek(w)}>
                <span className="week-block-title">Week {w}</span>
                <span className="week-block-count">{weekSessions.length} sessions</span>
                <span className="week-block-chevron">{isOpen ? '▲' : '▼'}</span>
              </div>
              {isOpen && (
                <div className="week-block-body">
                  {weekSessions.map(sess => (
                    <div key={sess.session_number} className="session-row">
                      <div className="session-label">
                        <span className="session-num">Session {sess.session_number}</span>
                        <span className="session-day">Day {sess.day_number}</span>
                      </div>
                      <div className="session-content">
                        {sess.units.length > 0 ? (
                          <>
                            <span className="session-units">
                              {sess.units.map(u => u.title).join(' · ')}
                            </span>
                            <span className="session-pages">pp. {sess.start_page}–{sess.end_page} ({sess.page_count} pp.)</span>
                          </>
                        ) : (
                          <span className="session-empty">No content assigned</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>

      <div className="actions">
        <button className="reset-btn" onClick={onReset}>Start Over</button>
      </div>
    </div>
  )
}
