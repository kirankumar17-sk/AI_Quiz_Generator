import React, { useState } from 'react'
import { generateQuiz } from '../services/api'
import QuizDisplay from '../components/QuizDisplay'

export default function GenerateQuizTab() {
  const [url, setUrl] = useState("")
  const [loading, setLoading] = useState(false)
  const [quiz, setQuiz] = useState(null)
  const [error, setError] = useState("")

  async function handleSubmit(e) {
    e.preventDefault()
    setError("")
    setQuiz(null)
    if (!/^https:\/\/en\.wikipedia\.org\/wiki\/.+/.test(url)) {
      setError("Please enter a valid Wikipedia article URL.")
      return
    }
    setLoading(true)
    try {
      const res = await generateQuiz(url)
      setQuiz(res)
    } catch (err) {
      setError(err.message || "Failed to generate quiz.")
    }
    setLoading(false)
  }

  return (
    <div style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <form className="form-container" onSubmit={handleSubmit}>
        <div style={{ display: 'flex', gap: '1rem', width: '100%', flexWrap: 'wrap' }}>
          <input
            type="url"
            className="form-input"
            placeholder="Enter Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/...)"
            value={url}
            onChange={e => setUrl(e.target.value)}
            required
            style={{ minWidth: '250px' }}
          />
          <button className="btn-primary" disabled={loading} style={{ whiteSpace: 'nowrap' }}>
            {loading ? (
              <>
                <span className="loading-spinner" style={{ marginRight: '0.5rem' }}></span>
                Generating...
              </>
            ) : (
              "Generate Quiz"
            )}
          </button>
        </div>
      </form>
      {error && <div className="error-message" style={{ maxWidth: '800px', width: '100%' }}>{error}</div>}
      {loading && (
        <div style={{ 
          textAlign: 'center', 
          padding: '3rem', 
          color: '#667eea',
          background: 'white',
          borderRadius: '1rem',
          boxShadow: 'var(--shadow-lg)',
          maxWidth: '500px',
          width: '100%',
          marginTop: '1rem'
        }}>
          <div className="loading-spinner" style={{ margin: '0 auto 1.5rem', width: '40px', height: '40px', borderWidth: '4px' }}></div>
          <div style={{ fontSize: '1.1rem', fontWeight: '600' }}>Generating your quiz...</div>
          <div style={{ fontSize: '0.9rem', color: '#9ca3af', marginTop: '0.5rem' }}>This may take a few moments</div>
        </div>
      )}
      {quiz && <div style={{ width: '100%', display: 'flex', justifyContent: 'center' }}><QuizDisplay quiz={quiz} /></div>}
    </div>
  )
}