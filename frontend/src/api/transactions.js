export async function getTransactions() {
    const url = `${import.meta.env.VITE_API_URL}/transactions`
    const response = await fetch(url)

    if (!response.ok) {
        throw new Error('Failed to fetch transactions')
    }

    return response.json()
}