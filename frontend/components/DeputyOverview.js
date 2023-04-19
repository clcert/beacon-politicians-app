import React from 'react'

const DeputyOverview = ({data}) => {
  const deputyName = `${ data.first_name } ${ data.first_surname }`

  return (
    <>
      <a href={data.photo} target='_blank' rel="noreferrer" className='image deputy-pic'>
        <img src={data.photo} alt={`Diputad${ data.termination } ${ deputyName }`} />
      </a>
      <h1>Diputad{ data.termination } <strong>{ data.first_name } { data.first_surname }</strong></h1>
      <h2>{ data.party }</h2>
      <div className='deputy-overview'>
        <p>
          {data.sex === '1' ? 'El diputado' : 'La diputada'} del día <strong>{data.date.split(' ')[0]}</strong> es{' '}
          <strong>{ data.first_name } { data.second_name } { data.first_surname } { data.second_surname }</strong>,{' '}
          nacid{ data.termination } el <strong>{ data.birthday }</strong>,{' '}
          {
            data.profession === 'Sin Información' ? '' : (
              <>es de profesión <strong>{ data.profession }</strong>, </>
            )
          }
          quien es actualmente diputad{ data.termination } por el <strong>distrito { data.district }</strong>{' '}
          que forma parte de la <strong>{ data.districtregion }</strong>,{' '}
          durante el período { data.lastperiod }.
        </p>
        <hr />
        <div className='parlamentary-periods'>
          <h4>Periodos Parlamentarios</h4>
          <div className='periods'>
            { data.periods.map((period, index) => <div key={index} className='period'>{period}</div>) }
          </div>
        </div>
      </div>
    </>
  )
}

export default DeputyOverview