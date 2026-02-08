// `App.jsx` — main React component for the GAA Stats client.
//
// Responsibilities:
// - Provide UI to add match events (team, minute, player, assistor, type)
// - Show calculated score and timeline of events
// - Allow clearing events and exporting to CSV
//
// Note: storage is provided by `db.js`. In a Capacitor native build this
// can be replaced with an on-device SQLite implementation.
import React, { useEffect, useState } from 'react'
import { addEvent, getEvents, clearEvents } from './db'
import { exportToCsv } from './utils'

function calcScore(events) {
  const scores = { Home: 0, Away: 0 }
  events.forEach((e) => {
    const val = e.type === 'Goal' ? 3 : 1
    scores[e.team] = (scores[e.team] || 0) + val
  })
  return scores
}

export default function App() {
  const [events, setEvents] = useState([])
  const [team, setTeam] = useState('Home')
  const [minute, setMinute] = useState(1)
  const [player, setPlayer] = useState('')
  const [assistor, setAssistor] = useState('')
  const [type, setType] = useState('Point')

  useEffect(() => {
    setEvents(getEvents())
  }, [])

  function handleAdd(e) {
    e.preventDefault()
    if (!player.trim()) return
    const ev = { team, minute: Number(minute), player: player.trim(), assistor: assistor.trim(), type }
    addEvent(ev)
    setEvents(getEvents())
    setPlayer('')
    setAssistor('')
  }

  function handleExport() {
    exportToCsv(events, 'events.csv')
  }

  function handleClear() {
    clearEvents()
    setEvents([])
  }

  const score = calcScore(events)

  return (
    <div className="container">
      <h1>GAA Stats App</h1>
      <div className="cols">
        <form className="card" onSubmit={handleAdd}>
          <h2>Add Event</h2>
          <label>Team</label>
          <select value={team} onChange={(e) => setTeam(e.target.value)}>
            <option>Home</option>
            <option>Away</option>
          </select>
          <label>Minute</label>
          <input type="number" min="0" max="120" value={minute} onChange={(e) => setMinute(e.target.value)} />
          <label>Player</label>
          <input value={player} onChange={(e) => setPlayer(e.target.value)} />
          <label>Assistor</label>
          <input value={assistor} onChange={(e) => setAssistor(e.target.value)} />
          <label>Type</label>
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option>Point</option>
            <option>Goal</option>
          </select>
          <div className="actions">
            <button type="submit">Add</button>
            <button type="button" onClick={handleClear}>Clear</button>
          </div>
        </form>

        <div className="card">
          <h2>Score</h2>
          <div className="score">
            <div>Home: <strong>{score.Home}</strong></div>
            <div>Away: <strong>{score.Away}</strong></div>
          </div>
          <h2>Timeline</h2>
          <div className="timeline">
            {events.length === 0 && <p>No events yet</p>}
            {events.sort((a,b)=>a.minute-b.minute).map((ev, i) => (
              <div className="event" key={i}>
                <div>{ev.minute}'</div>
                <div>{ev.team} — {ev.player} {ev.type === 'Goal' ? '(G)' : ''}</div>
                <div>{ev.assistor ? `Assist: ${ev.assistor}` : ''}</div>
              </div>
            ))}
          </div>
          <div className="actions">
            <button onClick={handleExport}>Export CSV</button>
          </div>
        </div>
      </div>
    </div>
  )
}
