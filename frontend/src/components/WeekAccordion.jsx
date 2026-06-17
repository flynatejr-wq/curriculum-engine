import { useState } from 'react'
import LessonRow from './LessonRow'

export default function WeekAccordion({ week, lessons, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen)

  return (
    <div className={`week-accordion${open ? ' week-accordion--open' : ''}`}>
      <div className="week-header" onClick={() => setOpen(o => !o)}>
        <span className="week-title">Week {week}</span>
        <span className="week-badge">{lessons.length} lessons</span>
        <span className="week-chevron">{open ? '▲' : '▼'}</span>
      </div>
      {open && (
        <div className="week-body">
          {lessons.map(entry => (
            <LessonRow key={entry.chunk_index} entry={entry} />
          ))}
        </div>
      )}
    </div>
  )
}
