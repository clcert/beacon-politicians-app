import React from 'react';

const DeputySelection = ({deputyName, selectionDate, gender, chainId, pulseId}) => {
  const datetime = new Date(selectionDate);
  const dateStr = datetime.toLocaleDateString('es-ES', {
    day: "numeric", 
    month: "long", 
    year: "numeric", 
    timeZone: "America/Santiago"
  });
  const depPronoun = gender === 'MALE' ? 'el diputado del día' : 'la diputada del día';
  const selected = gender === 'MALE' ? 'seleccionado' : 'seleccionada';

  return (
    <header className="major container medium">
      <h4>
        {deputyName} fue { selected } como { depPronoun } { dateStr } en base al Pulso&nbsp;
        <a href={`https://random.uchile.cl/beacon/2.0-beta1/chain/${ chainId }/pulse/${ pulseId }`} target='_blank' rel="noreferrer">
          #{ chainId }.{ pulseId }
        </a>{' '}
        del faro de aleatoriedad de Random UChile.
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