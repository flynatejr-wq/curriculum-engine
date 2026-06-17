import { useState } from 'react'

export default function LessonRow({ entry }) {
  const [open, setOpen] = useState(false)
  const { day, lesson } = entry

  return (
    <div className={`lesson-row${open ? ' lesson-row--open' : ''}`}>
      <div className="lesson-row-header" onClick={() => setOpen(o => !o)}>
        <span className="lesson-day">Day {day}</span>
        <span className="lesson-objective-preview">{lesson.objective}</span>
      </div>
      <div className="lesson-row-body" style={{ maxHeight: open ? '500px' : '0' }}>
        <div className="lesson-field">
          <span className="lesson-label">Objective</span>
          <p>{lesson.objective}</p>
        </div>
        <div className="lesson-field">
          <span className="lesson-label">Key Points</span>
          <ul className="lesson-key-points">
            {lesson.key_points.map((pt, i) => <li key={i}>{pt}</li>)}
          </ul>
        </div>
        <div className="lesson-field">
          <span className="lesson-chip lesson-chip--green">Activity</span>
          <p>{lesson.activity}</p>
        </div>
        <div className="lesson-field">
          <span className="lesson-chip lesson-chip--amber">Exit Ticket</span>
          <p>{lesson.exit_ticket}</p>
        </div>
      </div>
    </div>
  )
}
