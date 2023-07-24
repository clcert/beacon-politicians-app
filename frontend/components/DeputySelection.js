import React from 'react';
import { convertUTCDateToLocalDate } from '../utils/utils';

const DeputySelection = ({deputyName, date, selectionDate, gender, chainId, pulseId}) => {
  const datetime = convertUTCDateToLocalDate(new Date(date + ' 04:02:00'));
  const dateStr = datetime.toLocaleDateString('es-ES', {
    day: "numeric", 
    month: "long", 
    year: "numeric", 
    timeZone: "America/Santiago"
  });
  const updateDateStr = convertUTCDateToLocalDate(new Date(selectionDate)).toLocaleDateString('es-ES', {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "numeric",
    minute: "numeric",
    timeZone: "America/Santiago"
  });
  const depPronoun = gender === 'MALE' ? 'el diputado del día' : 'la diputada del día';
  const selected = gender === 'MALE' ? 'seleccionado' : 'seleccionada';

  return (
    <header className="major container medium">
      <h4>
        {deputyName} fue { selected } como { depPronoun } { dateStr } en base al Pulso&nbsp;
        <a href={`https://random.uchile.cl/beacon/2.0-beta1/chain/${ chainId }/pulse/${ pulseId }`} target='_blank' rel="noreferrer">
          #{ chainId }-{ pulseId }
        </a>{' '}
        del faro de aleatoriedad de Random UChile.
        <br/>
        <small className="update-timestamp">Los datos fueron consultados el {updateDateStr}.</small>
      </h4>
      <p className='verification-text'>
        Puedes comprobar la selección utilizando nuestro script (Python)&nbsp;
        <a href='https://github.com/clcert/beacon-politicians-app' target='_blank' rel="noreferrer">
          disponible en GitHub
        </a>.
      </p>
    </header>
  )
}

export default DeputySelection