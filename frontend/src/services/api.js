const API_BASE = "http://localhost:8000"

export async function generateQuiz(url) {
  const res = await fetch(`${API_BASE}/generate_quiz`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  })
  if (!res.ok) throw new Error(await res.text())
  return await res.json()
}

export async function listHistory() {
  const res = await fetch(`${API_BASE}/history`)
  if (!res.ok) throw new Error(await res.text())
  return await res.json()
}

export async function fetchQuiz(id) {
  const res = await fetch(`${API_BASE}/quiz/${id}`)
  if (!res.ok) throw new Error(await res.text())
  return await res.json()
}