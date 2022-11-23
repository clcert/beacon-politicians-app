import React from 'react';
import styles from '../styles/home/Overview.module.css';

const Overview = ({deputyInfo}) => {
  return (
    <div className='container'>
      <div className='row'>
        <div className='col-12'>
          <header className='major'>
            <p className={styles.selectionInfo}>
              Escogid{ deputyInfo.termination } el { deputyInfo.date } en base al Pulso&nbsp;
              <a href={`https://random.uchile.cl/beacon/2.0-beta1/chain/1/pulse/${ deputyInfo.record }`} target='_blank' rel="noreferrer">
                #{ deputyInfo.record }
              </a>
              <br/>
              Comprueba la elección utilizando nuestro script (Python)&nbsp;
              <a href='https://github.com/clcert/beacon-politicians-app' target='_blank' rel="noreferrer">
                disponible en GitHub
              </a>.
            </p>
          </header>
        </div>
      </div>
      <div className='row'>
        <div className='col-3 col-4-large col-12-medium'>
          <span className='image fit'>
            <a href={deputyInfo.photo} target='_blank' rel="noreferrer" className='image avatar'>
              <img src={deputyInfo.photo} alt={`Diputad${ deputyInfo.termination } ${ deputyInfo.first_name } ${ deputyInfo.first_surname }`} />
            </a>
          </span>
        </div>
        <div className='col-9 col-8-large col-12-medium'>
          <header>
            <h1 className={styles.name}>
              Diputad{ deputyInfo.termination } <strong>{ deputyInfo.first_name } { deputyInfo.first_surname }</strong>.
            </h1>
          </header>
          <p className={styles.partyDetail}>
            De la bancada { deputyInfo.party }.
          </p>
          <p id='intro'>
            <strong>{ deputyInfo.first_name } { deputyInfo.second_name } { deputyInfo.first_surname } { deputyInfo.second_surname }</strong>, 
            nacid{ deputyInfo.termination } el <strong>{ deputyInfo.birthday }</strong>, es de profesión <strong>{ deputyInfo.profession }</strong>,
            actualmente diputad{ deputyInfo.termination } por el <strong>distrito { deputyInfo.district }</strong> que forma parte de la <strong>{ deputyInfo.districtregion }</strong>,
            durante el período { deputyInfo.lastperiod }.
          </p>
          <hr />
          <div className={styles.parlamentaryPeriods}>
            <h3>Periodos Parlamentarios</h3>
            <div className={styles.periods}>
              { deputyInfo.periods.map((period, index) => <div key={index} className={styles.period}>{period}</div>) }
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Overview