import { useEffect, useState } from 'react'
import { getAccounts } from './api/accounts'
import { getTransactions, createTransaction } from './api/transactions'
import { getCategories } from './api/categories'

function App() {
  const [accounts, setAccounts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [transactions, setTransactions] = useState([])
  const [categories, setCategories] = useState([])
  const [date, setDate] = useState('')
  const [type, setType] = useState('expense')
  const [amount, setAmount] = useState('')
  const [description, setDescription] = useState('')
  const [categoryId, setCategoryId] = useState('')
  const [accountId, setAccountId] = useState('')
  const [fromAccountId, setFromAccountId] = useState('')
  const [toAccountId, setToAccountId] = useState('')

  const handleTypeChange = (event) => {
    setType(event.target.value)
    setCategoryId('')
    setAccountId('')
    setFromAccountId('')
    setToAccountId('')
    setError(null)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    if (!date) {
      setError('Please select a date')
      return
    }

    if (type !== 'transfer' && !accountId) {
      setError('Please select an account')
      return
    }

    if (!categoryId) {
      setError('Please select a category')
      return
    }

    if (type === 'transfer' && !fromAccountId) {
      setError('Please select a source account')
      return
    }

    if (type === 'transfer' && !toAccountId) {
      setError('Please select a destination account')
      return
    }

    if (!amount || Number(amount) <= 0) {
      setError('Please enter an amount greater than 0')
      return
    }

    if (type === 'transfer' && fromAccountId === toAccountId) {
      setError('Source and destination accounts must be different')
      return
    }

    const transaction = {
      date,
      type,
      amount: Number(amount),
      description,
      category_id: Number(categoryId),
      account_id: type === 'transfer' ? null : Number(accountId),
      from_account_id: type === 'transfer' ? Number(fromAccountId) : null,
      to_account_id: type === 'transfer' ? Number(toAccountId) : null
    }

    try {
      const createdTransaction = await createTransaction(transaction)

      setTransactions((currentTransactions) => [
        ...currentTransactions,
        createdTransaction
      ])

      const updatedAccounts = await getAccounts()
      setAccounts(updatedAccounts)

      setDate('')
      setAmount('')
      setDescription('')
      setCategoryId('')
      setAccountId('')
      setFromAccountId('')
      setToAccountId('')
      setError(null)
    } catch (error) {
      setError(error.message)
    }
  }

  useEffect(() => {
    Promise.all([
      getAccounts(),
      getTransactions(),
      getCategories()
    ])
      .then(([accounts, transactions, categories]) => {
        setAccounts(accounts)
        setTransactions(transactions)
        setCategories(categories)
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

      <form onSubmit={handleSubmit}>
        <label>
          Date
          <input
            type="date"
            value={date}
            onChange={(event) => setDate(event.target.value)}
          />
        </label>

        <label>
          Type
          <select
            value={type}
            onChange={handleTypeChange}
          >
            <option value="expense">Expense</option>
            <option value="income">Income</option>
            <option value="transfer">Transfer</option>
          </select>
        </label>

        <label>
          Amount
          <input
            type="number"
            min="0.01"
            step="0.01"
            value={amount}
            onChange={(event) => setAmount(event.target.value)}
          />
        </label>

        <label>
          Description
          <input
            type="text"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
          />
        </label>

        <label>
          Category
          <select
            value={categoryId}
            onChange={(event) => setCategoryId(event.target.value)}
          >
            <option value="">Select a category</option>

            {categories
              .filter((category) => category.type === type)
              .map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
          </select>
        </label>

        {type !== 'transfer' && (
          <label>
            Account
            <select
              value={accountId}
              onChange={(event) => setAccountId(event.target.value)}
            >
              <option value="">Select an account</option>

              {accounts.map((account) => (
                <option key={account.id} value={account.id}>
                  {account.name}
                </option>
              ))}
            </select>
          </label>
        )}

        {type === 'transfer' && (
          <label>
            From Account
            <select
              value={fromAccountId}
              onChange={(event) => setFromAccountId(event.target.value)}
            >
              <option value="">Select source account</option>

              {accounts.map((account) => (
                <option key={account.id} value={account.id}>
                  {account.name}
                </option>
              ))}
            </select>
          </label>
        )}

        {type === 'transfer' && (
          <label>
            To Account
            <select
              value={toAccountId}
              onChange={(event) => setToAccountId(event.target.value)}
            >
              <option value="">Select destination account</option>

              {accounts.map((account) => (
                <option key={account.id} value={account.id}>
                  {account.name}
                </option>
              ))}
            </select>
          </label>
        )}

        <button type="submit">Add Transaction</button>
      </form>

      {error && <p>Error: {error}</p>}

      <h2>Accounts</h2>

      {loading && <p>Loading accounts...</p>}

      {!loading && !error && (
        <ul>
          {accounts.map((account) => (
            <li key={account.id}>
              {account.name} &mdash; &#8369;{account.current_balance}
            </li>
          ))}
        </ul>
      )}

      <h2>Transactions</h2>

      <ul>
        {transactions.map((transaction) => {
          const account = accounts.find(
            (account) => account.id === transaction.account_id
          )

          const fromAccount = accounts.find(
            (account) => account.id === transaction.from_account_id
          )

          const toAccount = accounts.find(
            (account) => account.id === transaction.to_account_id
          )

          const category = categories.find(
            (category) => category.id === transaction.category_id
          )

          return (
            <li key={transaction.id}>
              {transaction.date} &mdash; {transaction.type} &mdash;{' '}
              {category?.name} &mdash; {transaction.description} &mdash;{' '}
              {transaction.type === 'transfer'
                ? `${fromAccount?.name} → ${toAccount?.name}`
                : account?.name}{' '}
              &mdash; &#8369;{Number(transaction.amount).toFixed(2)}
            </li>
          )
        })}
      </ul>
    </div>
  )
}

export default App