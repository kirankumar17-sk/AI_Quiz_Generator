import React, { useEffect, useState } from 'react'
import { listHistory, fetchQuiz } from '../services/api'
import QuizDisplay from '../components/QuizDisplay'
import Modal from '../components/Modal'

export default function HistoryTab() {
  const [history, setHistory] = useState([])
  const [selectedQuiz, setSelectedQuiz] = useState(null)
  const [modalOpen, setModalOpen] = useState(false)

  useEffect(() => {
    listHistory().then(setHistory)
  }, [])

  async function showDetails(id) {
    const quiz = await fetchQuiz(id)
    setSelectedQuiz(quiz)
    setModalOpen(true)
  }

  return (
    <div style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h2 style={{ fontWeight: '700', fontSize: '1.75rem', marginBottom: '2rem', color: '#1a202c', textAlign: 'center' }}>Quiz History</h2>
      <div className="card" style={{ overflowX: 'auto', width: '100%' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead style={{ background: 'linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%)' }}>
            <tr>
              <th style={{ padding: '0.75rem', textAlign: 'left', fontWeight: '600', color: '#667eea', borderBottom: '2px solid #667eea' }}>ID</th>
              <th style={{ padding: '0.75rem', textAlign: 'left', fontWeight: '600', color: '#667eea', borderBottom: '2px solid #667eea' }}>Title</th>
              <th style={{ padding: '0.75rem', textAlign: 'left', fontWeight: '600', color: '#667eea', borderBottom: '2px solid #667eea' }}>URL</th>
              <th style={{ padding: '0.75rem', textAlign: 'left', fontWeight: '600', color: '#667eea', borderBottom: '2px solid #667eea' }}>Date</th>
              <th style={{ padding: '0.75rem', textAlign: 'left', fontWeight: '600', color: '#667eea', borderBottom: '2px solid #667eea' }}>Details</th>
            </tr>
          </thead>
          <tbody>
            {history.map(h => (
              <tr key={h.id} style={{ borderTop: '1px solid #e2e8f0', transition: 'background 0.2s' }} 
                  onMouseEnter={(e) => e.currentTarget.style.background = '#f8f9ff'}
                  onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}>
                <td style={{ padding: '0.75rem' }}>{h.id}</td>
                <td style={{ padding: '0.75rem', fontWeight: '500' }}>{h.title}</td>
                <td style={{ padding: '0.75rem' }}>
                  <a href={h.url} style={{ color: '#667eea', textDecoration: 'none' }} target="_blank" rel="noopener noreferrer"
                     onMouseEnter={(e) => e.currentTarget.style.textDecoration = 'underline'}
                     onMouseLeave={(e) => e.currentTarget.style.textDecoration = 'none'}>
                    {h.url}
                  </a>
                </td>
                <td style={{ padding: '0.75rem', color: '#4a5568' }}>{new Date(h.date_generated).toLocaleString()}</td>
                <td style={{ padding: '0.75rem' }}>
                  <button className="btn-primary" style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }} onClick={() => showDetails(h.id)}>Details</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {history.length === 0 && (
          <div style={{ textAlign: 'center', padding: '3rem', color: '#9ca3af' }}>
            No quiz history yet. Generate your first quiz!
          </div>
        )}
      </div>
      <Modal open={modalOpen} onClose={() => setModalOpen(false)}>
        <QuizDisplay quiz={selectedQuiz} />
      </Modal>
    </div>
  )
}