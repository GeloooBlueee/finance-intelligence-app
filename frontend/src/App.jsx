import { useEffect, useState } from 'react'
import { getAccounts } from './api/accounts'

function App() {
  const [accounts, setAccounts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getAccounts()
    .then((data) => {
      setAccounts(data)
      setLoading(false)
    })
    .catch((error) => {
      setError(error.message)
      setLoading(false)
    })
  }, [])

  return (
    <div>
      <h1>Finance Intelligence</h1>

      <h2>Accounts</h2>

      {loading && <p>Loading accounts...</p>}
      {error && <p>Error: {error}</p>}
      {!loading && !error && (
        <ul>
          {accounts.map((account) => (
            <li key={account.id}>
              {account.name} &mdash;  &#8369;{account.initial_balance}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default App