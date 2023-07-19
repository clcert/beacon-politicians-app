import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';

const HistoryMonths = ({expenses}) => {
  const [ options, setOptions ] = useState({});
  const sorted_expenses = expenses.sort((a, b) => a.code > b.code ? 1 : -1);

  useEffect(() => {
    const monthsAxis = sorted_expenses.map(exp => exp.month.substring(0,3)+"-"+exp.year%100);
    let keys = Object.keys(sorted_expenses[0]).filter(
      key => key !== 'month' && key !== 'year' && key !== 'total' && key !== 'code' && key !== 'Personal de Apoyo'
    );
    let catMonthsData = keys.map(key => {
      return sorted_expenses.map(month => {
        return month[key].amount;
      });
    });
    const shortLabels = [
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
    const chartColors = [
      '#80FFA5', '#00DDFF', '#37A2FF', '#FF0087', '#FFBF00',
      '#FF3F00', '#FFD500', '#008E00', '#00AAAA', '#AA00AA',
      '#5574A6', '#FF0022'
  ]

    setOptions({
      color: chartColors,
      title: {
        text: 'Gastos Operacionales',
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
        data: shortLabels,
        show: false,
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: false,
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
            formatter: function (value, index) {
              return value/1000000 + 'M';
            },
          }
        }
      ],
      series: keys.map((_, index) => ({
        name: shortLabels[index],
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
        data: catMonthsData[index]
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
        <h3>Progresión de Gastos Operacionales</h3>
        <p>
          Se presenta además la evolución de los gastos operacionales en los 
          <strong> últimos 6 meses</strong><a href='#ref-6'><sup>6</sup></a> con registro.
        </p>
      </div>
    </>
  )
}

export default HistoryMonths