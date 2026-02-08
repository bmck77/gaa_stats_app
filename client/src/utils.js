// utils.js — small client utilities.
//
// `exportToCsv` creates and triggers a download of a CSV file in the browser.
// In a native Capacitor app prefer writing files via the Filesystem/Share plugins.
export function exportToCsv(rows, filename = 'data.csv') {
  if (!rows || !rows.length) return
  const header = Object.keys(rows[0])
  const csv = [header.join(',')].concat(rows.map(r => header.map(h => JSON.stringify(r[h] ?? '')).join(','))).join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.setAttribute('download', filename)
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
