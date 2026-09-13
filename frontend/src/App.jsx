import { useEffect, useState } from 'react'
import { getAccounts } from './api/accounts'
import { getTransactions } from './api/transactions'

function App() {
  const [accounts, setAccounts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [transactions, setTransactions] = useState([])

useEffect(() => {
    Promise.all([
        getAccounts(),
        getTransactions()
    ])
    .then(([accounts, transactions]) => {
        setAccounts(accounts)
        setTransactions(transactions)
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

      <h2>Transactions</h2>
      <ul>
        {transactions.map((transaction) => (
          <li key={transaction.id}>
            {transaction.date} &mdash; {transaction.type} &mdash; {transaction.description} &mdash; &#8369;{transaction.amount}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App