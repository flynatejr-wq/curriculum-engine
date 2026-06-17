import { useState } from 'react'
import Header from './components/Header'
import UploadPanel from './components/UploadPanel'
import CurriculumPanel from './components/CurriculumPanel'
import { uploadTextbook } from './api'

export default function App() {
  const [status, setStatus] = useState('idle')
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  async function handleSubmit(file, title) {
    setStatus('processing')
    setError(null)
    try {
      const result = await uploadTextbook(file, title)
      setData(result)
      setStatus('results')
    } catch (err) {
      setError(err.message)
      setStatus('idle')
    }
  }

  function handleReset() {
    setStatus('idle')
    setData(null)
    setError(null)
  }

  return (
    <div className="app">
      <Header />
      <main className="main">
        <UploadPanel status={status} onSubmit={handleSubmit} error={error} />
        {status === 'results' && data && (
          <CurriculumPanel data={data} onReset={handleReset} />
        )}
      </main>
    </div>
  )
}
