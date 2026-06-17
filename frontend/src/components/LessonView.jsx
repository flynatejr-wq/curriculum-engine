export default function LessonView({ lesson, onBack }) {
  return (
    <div className="lesson-view">
      <div className="lesson-nav">
        <button className="back-btn" onClick={onBack}>← Back to Schedule</button>
      </div>

      <div className="lesson-header">
        <div className="lesson-meta-row">
          <span className="lesson-badge">Week {lesson.week_number} · Day {lesson.day_number}</span>
          <span className="lesson-pages">{lesson.page_range}</span>
        </div>
        <h2 className="lesson-title">{lesson.title}</h2>
        {lesson.source_sections.length > 0 && (
          <p className="lesson-sections">{lesson.source_sections.join(' · ')}</p>
        )}
      </div>

      <div className="lesson-body">
        <section className="lesson-section">
          <h3 className="lesson-section-title">Learning Objectives</h3>
          <ol className="lesson-objectives">
            {lesson.learning_objectives.map((obj, i) => (
              <li key={i}>{obj}</li>
            ))}
          </ol>
        </section>

        <section className="lesson-section">
          <h3 className="lesson-section-title">Key Concepts</h3>
          <dl className="lesson-concepts">
            {lesson.key_concepts.map((kc, i) => (
              <div key={i} className="concept-row">
                <dt className="concept-term">{kc.term}</dt>
                <dd className="concept-def">{kc.definition}</dd>
              </div>
            ))}
          </dl>
        </section>

        <section className="lesson-section">
          <h3 className="lesson-section-title">Classroom Activities</h3>
          <div className="lesson-activities">
            {lesson.activities.map((act, i) => (
              <div key={i} className="activity-card">
                <div className="activity-card-header">
                  <span className="activity-title">{act.title}</span>
                  {act.duration_minutes && (
                    <span className="activity-duration">{act.duration_minutes} min</span>
                  )}
                </div>
                <p className="activity-desc">{act.description}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="lesson-section">
          <h3 className="lesson-section-title">Assessment Questions</h3>
          <ol className="lesson-questions">
            {lesson.assessment_questions.map((q, i) => (
              <li key={i} className="question-item">
                <span className="question-text">{q.question}</span>
                <span className={`question-type question-type--${q.type}`}>{q.type.replace('_', ' ')}</span>
              </li>
            ))}
          </ol>
        </section>

        {lesson.homework && (
          <section className="lesson-section">
            <h3 className="lesson-section-title">Homework</h3>
            <p className="lesson-homework">{lesson.homework}</p>
          </section>
        )}
      </div>
    </div>
  )
}
