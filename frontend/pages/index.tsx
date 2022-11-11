import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'

const deputyInfo = {
  'date': '2022-11-06 01:08:00',
  'index': 33,
  'record': 83707,
  'json_index': 0,
  'photo': 'https://www.camara.cl/img.aspx?prmID=GRCL1021',
  'profession': 'Sin Información',
  'district': 'Nº 7',
  'districtregion': 'Región de Valparaíso',
  'party': 'Renovación Nacional',
  'periods': [
    '2018-2022',
    '2022-2026'
  ],
  'lastperiod': '2022-2026',
  'first_name': 'Andrés',
  'second_name': '',
  'first_surname': 'Celis',
  'second_surname': 'Montt',
  'birthday': '08/04/1975',
  'sex': '1',
  'termination': 'o',
  'treatment': 'Sr',
  'deputy_id': 1021,
  'attendance': {
    'attended': 82,
    'justified': 10,
    'unjustified': 0,
    'total': 92,
    'percentage': 100.0
  },
  'voting': [
    {
      'vote_option': 'Afirmativo',
      'date': '2022-10-26',
      'name': 'Extiende transitoriamente el permiso postnatal parental.',
      'description': 'Boletín N° 15418-13',
      'voting_id': 39383
    },
    {
      'vote_option': 'Afirmativo',
      'date': '2022-10-26',
      'name': 'Extiende transitoriamente el permiso postnatal parental.',
      'description': 'Boletín N° 15418-13',
      'voting_id': 39382
    },
    {
      'vote_option': 'En Contra',
      'date': '2022-10-26',
      'name': 'Aprueba el ´Convenio Constitutivo de la Corporación Andina de Fomento´, el ´Convenio de suscripción de acciones de capital ordinario entre la Corporación Andina de Fomento y la República de Chile e incorporación de la República de Chile como país miembro´ y el ´Convenio de suscripción de acciones de capital de garantía entre la Corporación Andina de Fomento y la República de Chile´ adoptado el 7 de febrero de 1968 y suscritos con fecha 23 de junio de 2022, respectivamente.',
      'description': 'Boletín N° 15433-10',
      'voting_id': 39381
    },
    {
      'vote_option': 'Afirmativo',
      'date': '2022-10-26',
      'name': 'OTROS-Renuncia de los miembros de la Mesa.',
      'description': 'Otros',
      'voting_id': 39371
    },
    {
      'vote_option': 'Afirmativo',
      'date': '2022-10-24',
      'name': 'Introduce un nuevo Párrafo en el Título VII del Libro II del Código Penal, relativo a la explotación sexual comercial y material pornográfico de niños, niñas y adolescentes',
      'description': 'Boletín N° 14440-07',
      'voting_id': 39343
    },
    {
      'vote_option': 'Afirmativo',
      'date': '2022-10-24',
      'name': 'Declara el 26 de junio de cada año como el Día Nacional de Concientización sobre la Esclerosis Múltiple, de la Esclerosis Lateral Amiotrófica y de otras Enfermedades Desmielinizantes',
      'description': 'Boletín N° 14500-11',
      'voting_id': 39340
    },
    {
      'vote_option': 'Afirmativo',
      'date': '2022-10-18',
      'name': 'Aprueba el Acuerdo entre el Gobierno de la República de Chile y el Gobierno del Sultanato de Omán sobre Exención Mutua de Visa para Titulares de Pasaportes Diplomáticos, Especiales, de Servicio y Oficiales, suscrito en El Cairo, República Árabe de Egipto, el 22 de marzo de 2022',
      'description': 'Boletín N° 15152-10',
      'voting_id': 39319
    },
    {
      'vote_option': 'Afirmativo',
      'date': '2022-10-18',
      'name': 'Aprueba el Convenio sobre Seguridad Social entre la República de Chile y Rumanía, suscrito en Santiago, el 26 de febrero de 2021',
      'description': 'Boletín N° 15332-10',
      'voting_id': 39318
    },
    {
      'vote_option': 'Afirmativo',
      'date': '2022-10-18',
      'name': 'Aprueba el Convenio entre el Gobierno de la República de Chile y la Organización Europea para la Investigación Astronómica en el Hemisferio Austral, para regular el ejercicio de las actividades remuneradas por parte de familiares dependientes de funcionarios(as) internacionales de dicho organismo internacional, suscrito en Santiago, Chile, el 11 de diciembre de 2020',
      'description': 'Boletín N° 15331-10',
      'voting_id': 39317
    },
    {
      'vote_option': 'Afirmativo',
      'date': '2022-10-12',
      'name': 'Que dispone la publicidad de las sesiones de los concejos municipales',
      'description': 'Boletín N° 14250-06',
      'voting_id': 39291
    }
  ]
}

export default function Home() {

  return (
    <div>
      <Head>
        <link rel='shortcut icon' href='/favicon.ico' />
        <title>#DiputadoDelDia</title>
        <meta name='viewport' content='width=device-width, initial-scale=1, user-scalable=no' />
      </Head>
      <main>

        <nav id='nav'>
          <ul className='container'>
            <li><a href='#top'>Principal</a></li>
            <li><a href='#attendance'>Asistencia</a></li>
            <li><a href='#votes'>Votaciones</a></li>
          </ul>
        </nav>


        <article id='top' className='wrapper style1'>
          <div className='container'>
            <div className='row'>
              <div className='col-12'>
                <header className='major'>
                  <p className={styles.selectionInfo}>
                    Escogid{ deputyInfo.termination } el { deputyInfo.date } en base al Pulso&nbsp;
                    <a href={`https://random.uchile.cl/beacon/2.0-beta1/chain/1/pulse/${ deputyInfo.record }`} target='_blank'>
                      # { deputyInfo.record }
                    </a>
                    <br/>
                    Comprueba la elección utilizando nuestro script (Python)&nbsp;
                    <a href='https://github.com/clcert/beacon-politicians-app' target='_blank'>
                      disponible en GitHub
                    </a>.
                  </p>
                </header>
              </div>
            </div>
            <div className='row'>
              <div className='col-3 col-4-large col-12-medium'>
                <span className='image fit'>
                  <a href={deputyInfo.photo} target='_blank' className='image avatar'>
                    <img src={deputyInfo.photo} alt='Deputy Picture' />
                  </a>
                </span>
              </div>
              <div className='col-9 col-8-large col-12-medium'>
                <header>
                  <h1>
                    Diputad{ deputyInfo.termination } <strong>{ deputyInfo.first_name } { deputyInfo.first_surname }</strong>.
                  </h1>
                </header>
                <p className={styles.partyDetail}>
                  De la bancada de { deputyInfo.party }.
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
        </article>

        <article id='attendance' className='wrapper style2'>
          <div className='container'>
            <header>
              <h2>Asistencia</h2>
              <p>
                A la fecha de consulta, ha asistido a <strong>{ deputyInfo.attendance.attended } sesiones de cámara</strong>, 
                de un total de { deputyInfo.attendance.total } sesiones, obteniendo así un <strong>{ deputyInfo.attendance.percentage }% 
                de asistencia justificada</strong>. Considerando las inasistencias justificadas y las no justificadas
                <sup><a id='text-attendance' href='#ref-attendance'>1</a></sup>, se puede apreciar el siguiente gráfico:
              </p>
            </header>
            <div>
              <div id='graphicContainer'>
                <canvas id='attendanceChart' width='500' height='auto'></canvas>
              </div>
            </div>
          </div>
        </article>

        {/* <article id='votes' className='wrapper style3'>
          <div className='container'>
            <header>
              <h2>Votaciones</h2>
              <p>Se listan las votaciones en sala más recientes.</p>
            </header>
            <div className='row'>
              <table className='votes-table'>
                <tr>
                  <th>Fecha</th>
                  <th>Documento</th>
                  <th>Materia</th>
                  <th>Votación</th>
                  <th>Detalle</th>
                </tr>
                { 
                  deputyInfo.voting.map((vote, index) => {
                    return (
                      <tr>
                        <td>{ vote.date }</td>
                        <td>{ vote.description }</td>
                        <td>{ vote.name }</td>
                        <td>{ vote.vote_option }</td>
                        <td>
                          <a href={`https://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=${vote.voting_id}`} target='_blank'>
                            Ver
                          </a>
                        </td>
                      </tr>
                    )
                  })
                }
              </table>
            </div>
          </div>
        </article> */}

        <article id='contact' className='wrapper style4'>
          <div className='container medium'>
            <header>
              <h2>Referencias</h2>
                <ol>
                  <li id='ref-attendance'>
                    <sup><a href='#text-attendance'></a></sup> 
                    Cálculo hecho según justificaciones a inasistencias, para más información visitar:
                    <a href='https://opendata.camara.cl/camaradiputados/WServices/WSSala.asmx' target='_blank'>
                      https://opendata.camara.cl/camaradiputados/WServices/WSSala.asmx
                    </a>
                  </li>
                </ol>
            </header>

            <footer>
              <p>¿Quieres saber como funciona la elección del #DiputadoDelDía?
                <a href='#' target='_blank'> Descúbrelo aquí</a>.
              </p>
              <ul id='copyright'>
                <li>&copy; Untitled. All rights reserved.</li><li>Design: <a href='http://html5up.net'>HTML5 UP</a></li>
              </ul>
            </footer>
          </div>
        </article> 
      </main>
    </div>
  )
}
