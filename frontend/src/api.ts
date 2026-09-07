const BASE_URL = 'http://127.0.0.1:8000/api'

/**
 * 
 * @param path
 * @param options
 * @returns
 */
async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })

  if (!response.ok) {
    const body = await response.text().catch(() => '')
    throw new Error(`${response.status}: ${body || 'empty body'}`)
  }

  return response.json()
}

export const apiGet = <T>(path: string) =>
    request<T>(path)

export const apiPost = <T>(path: string, body: unknown) =>
    request<T>(path, { method: 'POST', body: JSON.stringify(body) })