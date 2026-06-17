import { useState } from 'react'

export default function App() {
  const [status, setStatus] = useState('idle')
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  return (
    <div className="app">
      <div className="main">
        <p style={{ padding: '80px 24px', color: 'var(--color-text-muted)' }}>
          State: {status}
        </p>
      </div>
    </div>
  )
}
