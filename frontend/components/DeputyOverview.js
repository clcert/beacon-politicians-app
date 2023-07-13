import React from 'react'

const DeputyOverview = ({profile, date}) => {
  const selectionDate = new Date(date);
  const bornDate = new Date(profile.birthdate);
  const selectionDateStr = selectionDate.toLocaleDateString('es-ES', {
    day: "numeric", 
    month: "long",
    timeZone: "America/Santiago"
  });
  const isMale = profile.gender === 'MALE';
  const deputyTitle = isMale ? 'Diputado' : 'Diputada';
  const titleWithPronoun = isMale ? 'El diputado' : 'La diputada';
  const shortName = `${ profile.first_name } ${ profile.first_surname }`;
  const fullName = `${ profile.first_name } ${ profile.first_surname } ${ profile.second_surname }`;
  const age = new Date().getFullYear() - bornDate.getFullYear();
  const lastPeriod = profile.periods[profile.periods.length].split('-');

  return (
    <>
      <a href={profile.picture} target='_blank' rel="noreferrer" className='image deputy-pic'>
        <img src={profile.picture} alt={`${ deputyTitle } ${ shortName }`} />
      </a>
      <h1>{ deputyTitle } <strong>{ shortName }</strong></h1>
      <h2>{ profile.party }</h2>
      <div className='deputy-overview'>
        <p>
          { titleWithPronoun } del día <strong>{ selectionDateStr }</strong> es{' '}
          <strong>{ fullName }</strong>. Con <strong>{ age } años</strong> de edad,{' '}
          {
            profile.profession === 'Sin Información' ? '' : (
              <>es de profesión <strong>{ profile.profession }</strong> y{' '}</>
            )
          }
          actualmente es { deputyTitle.toLocaleLowerCase() } por el <strong>distrito { profile.district }</strong>{' '}
          que forma parte de la <strong>{ profile.region }</strong>,{' '}
          durante el período { lastPeriod[0] } a { lastPeriod[1] }.
        </p>
        <hr />
        <div className='parlamentary-periods'>
          <h4>Periodos Parlamentarios</h4>
          <div className='periods'>
            { profile.periods.map((period, index) => <div key={index} className='period'>{period}</div>) }
          </div>
        </div>
      </div>
    </>
  )
}

export default DeputyOverview