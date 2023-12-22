import React from 'react';
import { convertUTCDateToLocalDate } from '../utils/utils';

const DeputyOverview = ({profile, date, deputy_id}) => {
  const selectionDate = convertUTCDateToLocalDate(new Date(date + ' 05:00:00'));
  const bornDate = new Date(profile.birthdate);
  const selectionDateStr = selectionDate.toLocaleDateString('es-ES', {
    day: "numeric", 
    month: "long",
    timeZone: "America/Santiago"
  });
  const isMale = profile.gender === 'MALE';
  const deputyTitle = isMale ? 'Diputado' : 'Diputada';
  const titleWithPronoun = isMale ? 'El diputado' : 'La diputada';
  const shortName = `${ profile.name } ${ profile.firstSurname }`;
  const fullName = `${ profile.name } ${ profile.firstSurname } ${ profile.secondSurname }`;
  const profileUrl = `https://www.camara.cl/diputados/detalle/biografia.aspx?prmID=${deputy_id}`
  const ordered_periods = profile.periods.sort()
  
  const delta = new Date(selectionDate - bornDate);
  const age = delta.getUTCFullYear() - 1970;

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
          actualmente es { deputyTitle.toLocaleLowerCase() } por el <strong>distrito { profile.district }</strong>{', '}
          que forma parte de la <strong>{ profile.region }</strong>.
        </p>
        <hr />
        <div className='parlamentary-periods'>
          <h4>Periodos Parlamentarios</h4>
          <div className='periods'>
            { ordered_periods.map((period, index) => <div key={index} className='period'>{ period[0] } a { period[1] }</div>) }
          </div>
        </div>
      </div>
    </>
  )
}

export default DeputyOverview