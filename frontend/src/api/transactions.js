export async function getTransactions() {
    const url = `${import.meta.env.VITE_API_URL}/transactions`
    const response = await fetch(url)

    if (!response.ok) {
        throw new Error('Failed to fetch transactions')
    }

    return response.json()
}

export async function createTransaction(transaction) {
    const url = `${import.meta.env.VITE_API_URL}/transactions`

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(transaction)
    })

    if(!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail)
    }

    return response.json()
}