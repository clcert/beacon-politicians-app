import { useEffect, useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowAltCircleRight, faArrowAltCircleLeft } from '@fortawesome/free-solid-svg-icons'

import Attendance from '../components/Attendance'
import Overview from '../components/Overview'
import Votings from '../components/Votings'

import styles from '../styles/Home.module.css'


const getLastDeputyInfo = async () => {
  const jsonData = await fetch(`http://127.0.0.1:5000/api/diputadodeldia`).then((res) => res.json());
  return jsonData;
}

export default function Home() {

  const [ deputyInfo, setDeputyInfo ] = useState({});
  const [ loading, setLoading ] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      getLastDeputyInfo().then((data) => {
        setDeputyInfo(data);
        setLoading(false);
      });
    }, 1000);
  }, []);

  const changeDeputy = (deputyId) => {
    setLoading(true);
    setTimeout(async () => {
      const jsonData = await fetch(`http://127.0.0.1:5000/api/diputado/${deputyId}`).then((res) => res.json());
      setDeputyInfo(jsonData);
      setLoading(false);
    }, 1000);
  }

  return (
    <div>
      <Head>
        <link rel='shortcut icon' href='/favicon.png' />
        <title>#DiputadxDelDía</title>
        <meta name='viewport' content='width=device-width, initial-scale=1, user-scalable=no' />
      </Head>

      <nav id='nav' className={styles.navBar}>
        <div className={styles.logo}>
          Diputadx del Día
        </div>
        <ul className={styles.navItems}>
          <li><a href='#top'>Principal</a></li>
          <li><a href='#attendance'>Asistencia</a></li>
          <li><a href='#votes'>Votaciones</a></li>
        </ul>
        <div className={styles.changeDeputy}>
          { 
            deputyInfo.json_index > 0 ?
            <div>
              <FontAwesomeIcon icon={faArrowAltCircleLeft} onClick={() => changeDeputy(deputyInfo.json_index - 1)} />
            </div>
            :
            <div className={styles.disabledButton}>
              <FontAwesomeIcon icon={faArrowAltCircleLeft} />
            </div>
          }
          { 
            deputyInfo.json_index < deputyInfo.ljson_index ?
            <div>
              <FontAwesomeIcon icon={faArrowAltCircleRight} onClick={() => changeDeputy(deputyInfo.json_index + 1)} />
            </div>
            :
            <div className={styles.disabledButton}>
              <FontAwesomeIcon icon={faArrowAltCircleRight} />
            </div>
          }
        </div>
      </nav>

      {
        loading ? <div>Cargando...</div>
        :
        <>
          <article id='top' className='wrapper style1'>
            <Overview deputyInfo={deputyInfo} />
          </article>

          <article id='attendance' className='wrapper style2'>
            <Attendance deputyInfo={deputyInfo} />
          </article>

          <article id='votes' className='wrapper style3'>
            <Votings deputyInfo={deputyInfo} />
          </article>

          <article id='contact' className='wrapper style4'>
            <div className='container medium'>
              <header>
                <h2>Referencias</h2>
                  <ol>
                    <li id='ref-attendance'>
                      <sup><a href='#text-attendance'></a></sup> 
                      Cálculo hecho según justificaciones a inasistencias, para más información visitar:&nbsp;
                      <a href='https://opendata.camara.cl/camaradiputados/WServices/WSSala.asmx' target='_blank' rel='noreferrer'>
                        https://opendata.camara.cl/camaradiputados/WServices/WSSala.asmx
                      </a>
                    </li>
                  </ol>
              </header>

              <footer>
                <p>¿Quieres saber como funciona la elección del #DiputadoDelDía?&nbsp;
                  <Link href='/about'>Descúbrelo aquí</Link>.
                </p>
                <ul id='copyright'>
                  <li>&copy;Design: <a href='http://html5up.net'>HTML5 UP</a></li>
                </ul>
              </footer>
            </div>
          </article>
        </>
      }
    </div>
  )
}
