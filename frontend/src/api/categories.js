export async function getCategories() {
    const url = `${import.meta.env.VITE_API_URL}/categories`
    const response = await fetch(url)

    if (!response.ok) {
        throw new Error('Failed to fetch categories')
    }

    return response.json()
}