export default function StructureView({ data, onReset }) {
  const { filename, total_pages, structure } = data
  const { detection_method, chapters, warnings } = structure

  return (
    <div className="structure-view">
      <div className="structure-header">
        <h2 className="structure-title">{filename}</h2>
        <p className="structure-meta">
          {total_pages} pages · {chapters.length} chapters detected · method: <code>{detection_method}</code>
        </p>
      </div>

      {warnings && warnings.length > 0 && (
        <div className="warnings">
          {warnings.map((w, i) => (
            <p key={i} className="warning">⚠️ {w}</p>
          ))}
        </div>
      )}

      <div className="chapter-list">
        {chapters.map((ch, i) => (
          <div key={i} className="chapter-card">
            <div className="chapter-header">
              <span className="chapter-title">{ch.title}</span>
              <span className="chapter-pages">pp. {ch.start_page}–{ch.end_page ?? '?'}</span>
            </div>
            {ch.sections && ch.sections.length > 0 && (
              <ul className="section-list">
                {ch.sections.map((s, j) => (
                  <li key={j} className="section-item">
                    {s.title}
                    <span className="section-page">p. {s.start_page}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>

      <div className="actions">
        <button className="reset-btn" onClick={onReset}>Upload Another</button>
      </div>
    </div>
  )
}
