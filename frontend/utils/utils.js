export const formatAmount = (amount) => {
  return '$'+amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

export const getMonthsForHistoryChart = (expenses) => {
  const operational_months = expenses.operational.map((expense) => expense.month).reverse()
  const offices_months = expenses.offices.map((expense) => expense.month).reverse()
  const staff_months = expenses.staff.map((expense) => expense.month).reverse()
  const months = [...new Set([...operational_months,...offices_months, ...staff_months])]
  return months
}

export const getExpensesForHistoryChart = (expenses, months) => {
  let expenses_by_month = {}
  for (let expense of expenses) {
    expenses_by_month[expense.month] = expense.total
  }
  return months.map((month) => expenses_by_month[month] || undefined)
}