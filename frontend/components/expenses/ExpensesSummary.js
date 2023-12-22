import React from 'react';

import { formatAmount } from '../../utils/utils';

const ExpensesSummary = ({expenses, gender, deputyName}) => {
  const isMale = gender === 'MALE';
  const depTitle = isMale ? 'el diputado ' : 'la diputada ';

  const expSorted = expenses.sort((a, b) => a.code < b.code ? 1 : -1);
  const expLastMonth = expSorted[0];
  const expLastMonthSt = expLastMonth.detail[0];
  const expLastMonthOp = expLastMonth.detail[1];
  const parlamentarySalary = 7012388;

  const centered = {
    'textAlign': 'center',
  }

  return (
    <>
      <p style={centered}>
        El último mes en el que { depTitle } <strong>{ deputyName }</strong> tiene gastos registrados
        {' '}corresponde a <strong>{expLastMonth.month} de {expLastMonth.year}</strong>.
        {' '}En dicho mes, {depTitle} destinó <strong>{formatAmount(expLastMonthOp.amount)}
        {' '}en gastos operacionales</strong><a href='#ref-3-operational'><sup>3</sup></a> y
        {' '}<strong>{formatAmount(expLastMonthSt.amount)} en personal de apoyo</strong>
        <a href='#ref-2-staff'><sup>2</sup></a>. Estas asignaciones son adicionales a la dieta parlamentaria, 
        {' '}cuyo monto bruto corresponde a <strong>{formatAmount(parlamentarySalary)}</strong> mensuales
        <a href='#ref-4-sallary'><sup>4</sup></a>. 
      </p>
      <p style={centered}>
        Sumando dieta y asignaciones, {deputyName} ha significado un gasto de
        {' '}<strong>{formatAmount(expLastMonth.total + parlamentarySalary)}</strong> en el mes 
        {' '}de {expLastMonth.month} de {expLastMonth.year}.
      </p>
    </>
  )
}

export default ExpensesSummary