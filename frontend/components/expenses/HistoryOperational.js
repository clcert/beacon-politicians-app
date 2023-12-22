import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { formatAmount, shortOpExpSubtype } from '../../utils/utils';

const HistoryOperational = ({expenses}) => {
  const [ options, setOptions ] = useState({});
  const expSorted = expenses.sort((a, b) => a.code < b.code ? 1 : -1);
  const expLastMonthOp = expSorted[0].detail[1];

  useEffect(() => {
    const months = expSorted.map(exp => exp.month.substring(0,3)+"-"+exp.year%100);
    const subtypes = expLastMonthOp.expenses.map(data => shortOpExpSubtype(data.subtype));
    let subtypesAmountByMonth = subtypes.map((_, typeIndex) => {
      return months.map((_, monthIndex) => {
        return expSorted[monthIndex].detail[1].expenses[typeIndex].amount;
      });
    });
    const chartColors = [
      '#80FFA5', '#00DDFF', '#37A2FF', '#FF0087', '#FFBF00',
      '#FF3F00', '#FFD500', '#008E00', '#00AAAA', '#AA00AA',
      '#5574A6', '#FF0022'
    ]

    setOptions({
      color: chartColors,
      title: {
        text: 'Historial Gastos Operacionales',
        left: 'center',
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          label: {
            backgroundColor: '#6a7985'
          }
        }
      },
      legend: {
        data: subtypes,
        show: true,
        bottom: -5,
        align: 'left',
        left: 0,
        // type: 'scroll',
        orient: 'horizontal',
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        top: '10%',
        bottom: '30%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: false,
          data: months,
          axisLabel: {
            rotate: 70,
          }
        }
      ],
      yAxis: [
        {
          type: 'value',
          axisLabel: {
            formatter: function (value, index) {
              return value/1000000 + 'M';
            },
          }
        }
      ],
      series: subtypes.map((_, index) => ({
        name: subtypes[index],
        type: 'line',
        stack: 'Total',
        smooth: true,
        lineStyle: {
          width: 0
        },
        showSymbol: false,
        areaStyle: {
          opacity: 0.8,
        },
        emphasis: {
          focus: 'series'
        },
        data: subtypesAmountByMonth[index],
        tooltip: {
          valueFormatter: function (value) {
            return formatAmount(value);
          }
        },
      })),
    });

    return () => setOptions({});
  }, [])

  return (
    <>
      <div className='image chart-container-3'>
        <ReactECharts option={options} />
      </div>
      <div className='content'>
        <h3>Gastos Operacionales</h3>
        <p>
          Se presenta además la evolución de los gastos operacionales en los 
          <strong> últimos 6 meses</strong><a href='#ref-3'><sup>3</sup></a> con registro.
        </p>
      </div>
    </>
  )
}

export default HistoryOperational