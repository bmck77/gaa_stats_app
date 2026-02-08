// sync.js — helper that posts local events to the Python FastAPI backend.
//
// Usage: import { syncEventsToServer } from './sync' and call with the
// local events array. `baseUrl` defaults to http://localhost:8000 for
// local development.
export async function syncEventsToServer(events, baseUrl = 'http://localhost:8000') {
  if (!events || !events.length) return { ok: true, inserted: 0 }
  try {
    const res = await fetch(`${baseUrl}/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(events),
    })
    if (!res.ok) {
      const txt = await res.text()
      return { ok: false, status: res.status, text: txt }
    }
    const data = await res.json()
    return { ok: true, ...data }
  } catch (err) {
    return { ok: false, error: String(err) }
  }
}
