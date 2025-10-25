import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'

function App() {
  const [length, setLength] = useState(12)
  const [res, setRes] = useState(null)
  const [loading, setLoading] = useState(false)

  const generate = async () => {
    setLoading(true)
    try {
      const r = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          length: Number(length),
          use_lower: true,
          use_upper: true,
          use_digits: true,
          use_symbols: true
        })
      })
      const data = await r.json()
      setRes(data)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      fontFamily: 'Segoe UI, sans-serif',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      background: 'linear-gradient(135deg, #6EE7B7 0%, #3B82F6 100%)',
      color: '#1E293B'
    }}>
      <div style={{
        background: 'white',
        padding: '40px',
        borderRadius: '16px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.2)',
        width: '360px',
        textAlign: 'center'
      }}>
        <h1 style={{ marginBottom: '20px' }}>🔐 Password Generator</h1>
        <label>Length:&nbsp;
          <input
            type="number"
            value={length}
            min="4"
            max="64"
            onChange={e => setLength(e.target.value)}
            style={{ width: '60px', textAlign: 'center' }}
          />
        </label>
        <br />
        <button
          onClick={generate}
          disabled={loading}
          style={{
            marginTop: '20px',
            padding: '10px 20px',
            background: '#3B82F6',
            border: 'none',
            borderRadius: '8px',
            color: 'white',
            cursor: 'pointer'
          }}
        >
          {loading ? 'Generating...' : 'Generate'}
        </button>
        {res && (
          <div style={{ marginTop: '20px' }}>
            <div><b>Password:</b> <code>{res.password}</code></div>
            {res.policy && (
              <div style={{ marginTop: '10px', fontSize: '14px' }}>
                <b>Entropy:</b> {res.policy.entropy_bits} bits<br />
                <b>Score:</b> {res.policy.score}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
