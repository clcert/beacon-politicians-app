import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';

import { formatAmount, shortOpExpSubtype } from '../../utils/utils';

const ExpensesSummary = ({expenses, gender, deputyName}) => {
  const isMale = gender === 'MALE';
  const deputy = isMale ? 'Diputado' : 'Diputada';
  const depTitle = isMale ? 'el diputado ' : 'la diputada ';

  const expSorted = expenses.sort((a, b) => a.code < b.code ? 1 : -1);
  const expLastMonth = expSorted[0];
  const expLastMonthOp = expLastMonth.detail[1];

  const [options, setOptions] = useState({});

  useEffect(() => {
    const opLabels = expLastMonthOp.expenses.map(exp => shortOpExpSubtype(exp.subtype));
    const opValues = expLastMonthOp.expenses.map(exp => Math.round(exp.amount));
    const opAvg = expLastMonthOp.expenses.map(exp => Math.round(exp.deputiesAvg));
    // const opMin = expLastMonthOp.map(exp => Math.round(exp.deputiesMin));
    // const opMax = expLastMonthOp.map(exp => Math.round(exp.deputiesMax));

    setOptions({
      title: {
        text: `Gastos Operacionales\n${expLastMonth.month} de ${expLastMonth.year}`,
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
        bottom: 15,
        align: 'left',
        right: 10,
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '14%',
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
        data: opLabels,
        axisLabel: {
          rotate: 70,
        }
      },
      series: [
        {
          name: 'Gastos '+deputy,
          type: 'bar',
          data: opValues,
          tooltip: {
            valueFormatter: function (value) {
              return formatAmount(value);
            }
          },
        },
        {
          name: 'Promedio Cámara',
          type: 'bar',
          data: opAvg,
          tooltip: {
            valueFormatter: function (value) {
              return formatAmount(value);
            }
          },
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
        <h3>Distribución Operacionales</h3>
        <p>
          El el mes de <strong>{expLastMonth.month} de {expLastMonth.year}</strong> {depTitle} {deputyName}
          {' '}destinó <strong>{formatAmount(expLastMonthOp.amount)}</strong> en gastos operacionales
          <a href='#ref-3-operational'><sup>3</sup></a>, lo que lo ubica
          {' '}en el <strong>lugar número {expLastMonthOp.deputiesRanking}</strong> entre los diputados 
          {' '}con más gastos operacionales.<br/>
        </p>
      </div>
    </>
  )
}

export default ExpensesSummary