import { useEffect, useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowAltCircleRight, faArrowAltCircleLeft } from '@fortawesome/free-solid-svg-icons'
import DatePicker from 'react-datepicker'

import Attendance from '../components/Attendance'
import Overview from '../components/Overview'
import Votings from '../components/Votings'

import Expenses from '../components/Expenses'
import styles from '../styles/Home.module.css'
import 'react-datepicker/dist/react-datepicker.css'

const BACKEND_URI = 'http://127.0.0.1:5000'

const getLastDeputyInfo = async () => {
  const jsonData = await fetch(`${BACKEND_URI}/api/diputadodeldia`).then((res) => res.json());
  return jsonData;
}

export default function Home() {

  const [ deputyInfo, setDeputyInfo ] = useState({});
  const [ loading, setLoading ] = useState(true);
  const [ startDate, setStartDate ] = useState(new Date());
  const [ error, setError ] = useState(false);

  const getData = async (url) => {
    const dataJson = fetch(url)
      .then((res) => {
        if (res.status === 200) {
          setError(false);
          return res.json();
        }
        setError(true);
        return null;
      })
      .catch(() => {
        setError(true)
        return null;
      });
    return dataJson;
  }

  const getDeputyInfo = (url) => {
    setLoading(true);
    setTimeout(async () => {
      const jsonData = await getData(url);
      setDeputyInfo(jsonData);
      setLoading(false);
    }, 1000);
  }

  useEffect(() => {
    getDeputyInfo(`${BACKEND_URI}/api/diputadodeldia`);
  }, []);

  const changeDeputy = (date) => {
    setStartDate(date);
    const dateStr = date.toISOString().split('T')[0];
    getDeputyInfo(`${BACKEND_URI}/api/diputado/date/${dateStr}`);
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
          <img src='images/logo.png' alt='Diputadx del Día'/>
        </div>
        <ul className={styles.navItems}>
          <li><a href='#top'>Principal</a></li>
          <li><a href='#attendance'>Asistencia</a></li>
          <li><a href='#expenses'>Gastos</a></li>
          <li><a href='#votes'>Votaciones</a></li>
        </ul>
        <div className={styles.changeDeputy}>
          <DatePicker 
            className='datepicker'
            dateFormat="dd/MM/yyyy"
            selected={startDate}
            onChange={changeDeputy}
          />
        </div>
      </nav>

      {
        loading ? <div>Cargando...</div>
        :
        error ? <div>Hubo un error al cargar los datos</div>
        :
        <div className='articles'>
          <article id='top' className='wrapper style1'>
            <Overview deputyInfo={deputyInfo} />
          </article>

          <article id='attendance' className='wrapper style2'>
            <Attendance deputyInfo={deputyInfo} />
          </article>

          <article id='expenses' className='wrapper style3'>
            <Expenses deputyInfo={deputyInfo} />
          </article>

          <article id='votes' className='wrapper style2'>
            <Votings deputyInfo={deputyInfo} />
          </article>

          <article id='contact' className='wrapper style4'>
            <div className='container medium'>
              <header>
                <h2>Referencias</h2>
                  <ol>
                    <li id='ref-attendance'>
                      Cálculo hecho según justificaciones a inasistencias, para más información visitar: <br />
                      <a href='https://opendata.camara.cl/camaradiputados/WServices/WSSala.asmx' target='_blank' rel='noreferrer'>
                        https://opendata.camara.cl/camaradiputados/WServices/WSSala.asmx
                      </a>.
                    </li>
                    <li id='op-expenses'>
                      Los datos acerca de los gastos operacionales fueron obtenidos desde:<br />
                      <a href={`https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx?prmId=${deputyInfo.deputy_id}`} target='_blank' rel='noreferrer'>
                        {`https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx?prmId=${deputyInfo.deputy_id}`}
                      </a>.
                    </li>
                    <li id='of-expenses'>
                      Los datos acerca de los gastos en oficinas parlamentarias fueron obtenidos desde:<br />
                      <a href='https://www.camara.cl/transparencia/oficinasparlamentarias.aspx' target='_blank' rel='noreferrer'>
                        https://www.camara.cl/transparencia/oficinasparlamentarias.aspx
                      </a>.
                    </li>
                    <li id='st-expenses'>
                      Los datos acerca de los gastos de personal de apoyo fueron obtenidos desde:<br />
                      <a href='https://www.camara.cl/transparencia/personalapoyogral.aspx' target='_blank' rel='noreferrer'>
                        https://www.camara.cl/transparencia/personalapoyogral.aspx
                      </a>.
                    </li>
                    <li id='ref-expenses'>
                      Existen desfases con respecto a los meses con gastos declarados.
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
        </div>
      }
    </div>
  )
}
