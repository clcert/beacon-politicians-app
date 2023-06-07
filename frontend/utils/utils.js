export const BACKEND_URL = 'http://127.0.0.1:5000';

export const formatAmount = (amount) => {
  return '$'+amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

export const getMonthsForHistoryChart = (expenses) => {
  const operational_months = expenses.operational.map((expense) => expense.month).reverse()
  const offices_months = expenses.offices.map((expense) => expense.month).reverse()
  const staff_months = expenses.staff.map((expense) => expense.month).reverse()
  const months = [...new Set([...operational_months, ...staff_months])]
  return months
}

export const getExpensesForHistoryChart = (expenses, months) => {
  let expenses_by_month = {}
  for (let expense of expenses) {
    expenses_by_month[expense.month] = expense.total
  }
  return months.map((month) => expenses_by_month[month] || undefined)
}

export const getData = async (url) => {
  const dataJson = fetch(url)
    .then((res) => {
      if (res.status === 200) {
        return res.json();
      }
      return null;
    })
    .catch(() => {
      return null;
    });
  return dataJson;
}