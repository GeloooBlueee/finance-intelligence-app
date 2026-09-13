export async function getAccounts() {
  const url = `${import.meta.env.VITE_API_URL}/accounts`

  const response = await fetch(url)

  if (!response.ok) {
    throw new Error('Failed to fetch accounts')
  }

  return response.json()
}