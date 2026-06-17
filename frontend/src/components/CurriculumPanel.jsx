import WeekAccordion from './WeekAccordion'

export default function CurriculumPanel({ data, onReset }) {
  const byWeek = data.preview.reduce((acc, entry) => {
    const w = entry.week
    if (!acc[w]) acc[w] = []
    acc[w].push(entry)
    return acc
  }, {})

  const weeks = Object.keys(byWeek)
    .map(Number)
    .sort((a, b) => a - b)

  return (
    <div className="curriculum-panel">
      <div className="summary-bar">
        {data.title} · {data.total_chunks} chunks · {data.lessons_generated} lessons generated
      </div>
      <div className="curriculum-weeks">
        {weeks.map(w => (
          <WeekAccordion
            key={w}
            week={w}
            lessons={byWeek[w]}
            defaultOpen={w === 1}
          />
        ))}
      </div>
      <div className="curriculum-footer">
        <button className="reset-btn" onClick={onReset}>Upload another textbook</button>
      </div>
    </div>
  )
}
