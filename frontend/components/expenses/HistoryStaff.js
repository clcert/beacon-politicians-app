import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { formatAmount } from '../../utils/utils';

const HistoryStaff = ({expenses, gender}) => {
  const [ options, setOptions ] = useState({});
  const sortedExpenses = expenses.sort((a, b) => a.code > b.code ? 1 : -1);
  const isMale = gender === 'MALE';
  const deputy = isMale ? 'Diputado' : 'Diputada';

  useEffect(() => {
    const monthsAxis = sortedExpenses.map(exp => exp.month.substring(0,3)+"-"+exp.year%100);
    const amountMonthData = sortedExpenses.map(month => month.detail[0].amount);
    const averageMonthData = sortedExpenses.map(month => month.detail[0].deputiesAvg);
    
    const labels = ['Monto'];
    const chartColors = [ '#00DDFF']

    setOptions({
      color: chartColors,
      title: {
        text: 'Historial Personal de Apoyo',
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
        data: labels,
        show: false,
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      grid: {
        left: '10%',
        right: '10%',
        top: '20%',
        bottom: '20%',
      },
      xAxis: [
        {
          type: 'category',
          data: monthsAxis,
          axisLabel: {
            rotate: 70,
          }
        }
      ],
      yAxis: [
        {
          type: 'value',
          axisLabel: {
            formatter: function (value, _) {
              return value/1000000 + 'M';
            },
          }
        },
      ],
      series: [
        {
          name: deputy,
          type: 'line',
          data: amountMonthData,
          tooltip: {
            valueFormatter: function (value) {
              if (value > 0) {
                return formatAmount(value);
              }
              return 'Sin Información';
            }
          },
        },
        {
          name: 'Promedio Cámara',
          type: 'line',
          data: averageMonthData,
          tooltip: {
            valueFormatter: function (value) {
              if (value > 0) {
                return formatAmount(value);
              }
              return 'Sin Información';
            }
          },
        }
      ]
    });

    return () => setOptions({});
  }, [])

  return (
    <>
      <div className='image chart-container-4'>
        <ReactECharts option={options} />
      </div>
      <div className='content'>
        <h3>Personal de Apoyo</h3>
        <p>
          Según el número de personas contratadas como personal de apoyo,
          se destina un monto cada mes. En el gráfico adjunto se 
          presenta la evolución de los gastos en personal de apoyo para los
          <strong> últimos 6 meses</strong><a href='#ref-2-staff'><sup>2</sup></a> con información.
        </p>
      </div>
    </>
  )
}

export default HistoryStaff