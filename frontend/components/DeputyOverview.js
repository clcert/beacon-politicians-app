import React from 'react'

const DeputyOverview = ({profile, date, deputy_id}) => {
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
  const shortName = `${ profile.name } ${ profile.first_surname }`;
  const fullName = `${ profile.name } ${ profile.first_surname } ${ profile.second_surname }`;
  const age = new Date().getFullYear() - bornDate.getFullYear();
  const profileUrl = `https://www.camara.cl/diputados/detalle/biografia.aspx?prmID=${deputy_id}`

  return (
    <>
      <a href={profile.picture} target='_blank' rel="noreferrer" className='image deputy-pic'>
        <img src={profile.picture} alt={`${ deputyTitle } ${ shortName }`} />
      </a>
      <h1><a href={profileUrl} target='_blank'>{ deputyTitle } { shortName }</a></h1>
      <h2>{ profile.party }</h2>
      <div className='deputy-overview'>
        <p>
          { titleWithPronoun } del día <strong>{ selectionDateStr }</strong> es{' '}
          <strong>{ fullName }</strong>. Con <strong>{ age } años</strong> de edad,{' '}
          {/* {
            profile.profession === 'Sin Información' ? '' : (
              <>es de profesión <strong>{ profile.profession }</strong> y{' '}</>
            )
          } */}
          actualmente es { deputyTitle.toLocaleLowerCase() } por el <strong>distrito { profile.district }</strong>{' '}
          que forma parte de la <strong>{ profile.region }</strong>.
        </p>
        <hr />
        <div className='parlamentary-periods'>
          <h4>Periodos Parlamentarios</h4>
          <div className='periods'>
            { profile.periods.map((period, index) => <div key={index} className='period'>{ period[0] } a { period[1] }</div>) }
          </div>
        </div>
      </div>
    </>
  )
}

export default DeputyOverview