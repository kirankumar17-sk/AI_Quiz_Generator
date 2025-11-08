import React from 'react'

export default function QuizDisplay({ quiz }) {
  if (!quiz) return null
  return (
    <div className="card">
      <h2 className="quiz-title">{quiz.article_title}</h2>
      <p className="quiz-summary">{quiz.summary}</p>
      {quiz.key_entities?.length > 0 && (
        <div style={{ marginBottom: '0.5rem', padding: '0.5rem', background: '#f8f9fa', borderRadius: '0.5rem' }}>
          <span style={{ fontWeight: '600', color: '#667eea' }}>Key Entities:</span> {quiz.key_entities.join(', ')}
        </div>
      )}
      {quiz.related_topics?.length > 0 && (
        <div style={{ marginBottom: '1rem', padding: '0.5rem', background: '#f8f9fa', borderRadius: '0.5rem' }}>
          <span style={{ fontWeight: '600', color: '#667eea' }}>Related Topics:</span> {quiz.related_topics.join(', ')}
        </div>
      )}
      <h3 style={{ fontWeight: '600', marginBottom: '1rem', fontSize: '1.25rem', color: '#1a202c' }}>Quiz Questions</h3>
      <ol style={{ listStyle: 'decimal', paddingLeft: '1.5rem' }}>
        {quiz.questions.map((q, i) => (
          <li key={i} className="quiz-question">
            <div style={{ fontWeight: '700', marginBottom: '0.75rem', fontSize: '1.1rem' }}>{q.question}</div>
            <ul style={{ listStyle: 'disc', marginLeft: '1.5rem', marginBottom: '0.75rem' }}>
              {q.options.map((o, j) => (
                <li key={j} style={{ marginBottom: '0.25rem' }}>{o}</li>
              ))}
            </ul>
            <div className="quiz-answer">
              Answer: <span style={{ fontWeight: '600' }}>{q.answer}</span>
            </div>
            {q.explanation && (
              <div style={{ marginTop: '0.5rem', color: '#4a5568', fontSize: '0.875rem', fontStyle: 'italic' }}>
                Explanation: {q.explanation}
              </div>
            )}
          </li>
        ))}
      </ol>
    </div>
  )
}