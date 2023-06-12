import React from 'react'

const DeputyOverview = ({data}) => {
  const deputyName = `${ data.first_name } ${ data.first_surname }`
  const selectionDate = new Date(data.date);
  const bornDate = new Date(data.birthday);
  const selectionDateStr = selectionDate.toLocaleDateString('es-ES', {
    day: "numeric", 
    month: "long",
    timeZone: "America/Santiago"
  });
  const isMale = data.sex === '1';
  const deputyTitle = isMale ? 'Diputado' : 'Diputada';
  const titleWithPronoun = isMale ? 'El diputado' : 'La diputada';
  const shortName = `${ data.first_name } ${ data.first_surname }`;
  const fullName = `${ data.first_name } ${ data.second_name } ${ data.first_surname } ${ data.second_surname }`;
  const age = new Date().getFullYear() - bornDate.getFullYear();
  const lastPeriod = data.lastperiod.split('-');

  return (
    <>
      <a href={data.photo} target='_blank' rel="noreferrer" className='image deputy-pic'>
        <img src={data.photo} alt={`Diputad${ data.termination } ${ deputyName }`} />
      </a>
      <h1>{ deputyTitle } <strong>{ shortName }</strong></h1>
      <h2>{ data.party }</h2>
      <div className='deputy-overview'>
        <p>
          { titleWithPronoun } del día <strong>{ selectionDateStr }</strong> es{' '}
          <strong>{ fullName }</strong> con <strong>{ age } años</strong> de edad
          {
            data.profession === 'Sin Información' ? '' : (
              <> y es de profesión <strong>{ data.profession }</strong>.</>
            )
          }
          . Actualmente es { deputyTitle.toLocaleLowerCase() } por el <strong>distrito { data.district }</strong>{' '}
          que forma parte de la <strong>{ data.districtregion }</strong>,{' '}
          durante el período { lastPeriod[0] } a { lastPeriod[1] }.
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