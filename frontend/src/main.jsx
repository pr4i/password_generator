import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'

function App() {
  const [length, setLength] = useState(12)
  const [res, setRes] = useState(null)

  const generate = async () => {
    const r = await fetch('http://localhost:8000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        length: Number(length),
        use_lower: true, use_upper: true, use_digits: true, use_symbols: true
      })
    })
    const data = await r.json()
    setRes(data)
  }

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: 600, margin: '40px auto' }}>
      <h1>Password Generator</h1>
      <label>Length: <input type="number" value={length} onChange={e=>setLength(e.target.value)} /></label>
      <button onClick={generate} style={{ marginLeft: 12 }}>Generate</button>
      {res && (
        <div style={{ marginTop: 20 }}>
          <div><b>Password:</b> {res.password}</div>
          {res.policy && <div>
            <b>Entropy:</b> {res.policy.entropy_bits} bits &nbsp;|&nbsp;
            <b>Score:</b> {res.policy.score}
          </div>}
        </div>
      )}
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)