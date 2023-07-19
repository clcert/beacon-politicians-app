import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';

import { formatAmount } from '../../utils/utils';

const ExpensesSummary = ({expenses, gender, deputyName}) => {
  const isMale = gender === 'MALE';
  const deputy = isMale ? 'Diputado' : 'Diputada';
  const depPronoun = isMale ? 'del diputado ' : 'de la diputada ';
  const depTitle = isMale ? 'el diputado ' : 'la diputada ';

  const sorted_expenses = expenses.sort((a, b) => a.code < b.code ? 1 : -1);
  const last_month_exp = sorted_expenses[0];

  const [options, setOptions] = useState({});

  useEffect(() => {
    const expenses_labels = Object.keys(sorted_expenses[0]).filter(key => key !== 'month' && key !== 'year' && key !== 'total' && key !== 'code');
    const expenses_values = expenses_labels.map(label => sorted_expenses[0][label].amount);
    const expenses_average = expenses_labels.map(label => sorted_expenses[0][label].deputies_avg);
    const short_labels = [
      'Personal de Apoyo',
      'Web y Almacenamiento',
      'Traspaso a Personal de Apoyo',
      'Traslación y Bencina',
      'Telefonía',
      'Seguros',
      'Otros Gastos Oficina',
      'Otros',
      'Difusión',
      'Correspondencia',
      'Consumos Básicos',
      'Arriendo de Oficina',
      'Interacción Comunidad',
    ]

    setOptions({
      title: {
        text: `Gastos de ${last_month_exp.month}, ${last_month_exp.year}`,
        left: 'center',
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      legend: {
        top: 25,
        align: 'right',
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      yAxis: {
        type: 'value',
        boundaryGap: [0, 0.01],
        axisLabel: {
          formatter: function (value, index) {
            return value/1000000 + 'M';
          },
        }
      },
      xAxis: {
        type: 'category',
        data: short_labels,
        axisLabel: {
          rotate: 70,
        }
      },
      series: [
        {
          name: 'Gastos '+deputy,
          type: 'bar',
          data: expenses_values
        },
        {
          name: 'Promedio Diputados',
          type: 'bar',
          data: expenses_average
        }
      ]
    });
    return () => setOptions({});
  }, []);

  return (
    <>
      <div className='image chart-container-2'>
        <ReactECharts option={options} />
      </div>
      <div className='content'>
        <h3>Más Reciente</h3>
        <p>
          El último mes donde existe un registro de los gastos { depPronoun } <strong>{ deputyName }</strong>
          {' '}corresponde a <strong>{last_month_exp.month} de {last_month_exp.year}</strong>. En dicho mes,
          {' '+depTitle} destinó <strong>{formatAmount(last_month_exp.total)}</strong> entre gastos operacionales
          {' '}y personal de apoyo<a href='#ref-2'><sup>2,3</sup></a>.
          <br/>
          Estas asignaciones son adicionales a la dieta parlamentaria, cuyo monto bruto corresponde a 
          <strong> $7.012.388</strong> mensuales<a href='#ref-2'><sup>4</sup></a>.
        </p>
      </div>
    </>
  )
}

export default ExpensesSummary