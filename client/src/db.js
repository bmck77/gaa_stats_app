/*
  db.js — simple storage abstraction for the client.

  Current implementation: uses browser localStorage for quick prototyping.
  When packaging as a Capacitor-native app, replace this module with a
  native-backed implementation using `@capacitor-community/sqlite` so
  data is stored persistently on-device.

  API:
  - getEvents(): returns an array of stored events
  - addEvent(ev): append an event
  - clearEvents(): remove all events
*/

const KEY = 'gaa_events_v1'

export function getEvents() {
  try {
    const raw = localStorage.getItem(KEY)
    return raw ? JSON.parse(raw) : []
  } catch (e) {
    return []
  }
}

export function addEvent(ev) {
  const items = getEvents()
  items.push(ev)
  localStorage.setItem(KEY, JSON.stringify(items))
}

export function clearEvents() {
  localStorage.removeItem(KEY)
}
