import { forwardRef, useCallback, useEffect, useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import Image from 'next/image';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCalendarAlt } from '@fortawesome/free-solid-svg-icons';
import DatePicker from 'react-datepicker';

import Attendance from '../components/Attendance';
import Overview from '../components/Overview';
import Votings from '../components/Votings';

import Expenses from '../components/Expenses';
import styles from '../styles/Home.module.css';
import 'react-datepicker/dist/react-datepicker.css';

import logo from '../public/images/logo.png';

const BACKEND_URI = 'http://127.0.0.1:5000';

const CustomDatePicker = forwardRef(({ value, onClick }, ref) => (
  <button className="custom-datepicker-button" onClick={onClick} ref={ref}>
    <FontAwesomeIcon icon={faCalendarAlt} />
    {value}
  </button>
));
CustomDatePicker.displayName = 'CustomDatePicker';

export default function Home() {

  const [ deputyInfo, setDeputyInfo ] = useState({});
  const [ loading, setLoading ] = useState(true);
  const [ startDate, setStartDate ] = useState(new Date());
  const [ error, setError ] = useState(false);
  const [ datesError, setDatesError ] = useState(false);
  const [ availableDates, setAvailableDates ] = useState([]);

  const isValidDate = (date) => {
    return availableDates.filter((d) => d.toISOString().split('T')[0] === date.toISOString().split('T')[0]).length > 0;
  };

  const getData = async (url) => {
    const dataJson = fetch(url)
      .then((res) => {
        if (res.status === 200) {
          return res.json();
        }
        return null;
      })
      .catch(() => {
        return null;
      });
    return dataJson;
  }

  const getDeputyInfo = useCallback((url) => {
    setLoading(true);
    setTimeout(async () => {
      const jsonData = await getData(url);
      if (jsonData === null) {
        setError(true);
      } else {
        setError(false);
        setDeputyInfo(jsonData);
      }
      setLoading(false);
    }, 1000);
  }, [setError, setDeputyInfo, setLoading]);

  const getAvailableDates = useCallback(() => {
    setTimeout(async () => {
      const jsonData = await getData(`${BACKEND_URI}/api/dates`);
      if (jsonData === null) {
        setDatesError(true);
      } else {
        setDatesError(false);
        const data = jsonData.dates.map((date) => new Date(date));
        setAvailableDates(data);
        setStartDate(data[data.length - 1])
      }
    }, 1000);
  }, [setDatesError, setAvailableDates]);

  useEffect(() => {
    getDeputyInfo(`${BACKEND_URI}/api/diputadodeldia`);
    getAvailableDates();
  }, [getDeputyInfo, getAvailableDates]);

  const changeDeputy = (date) => {
    const offset = date.getTimezoneOffset()
    const offsetDate = new Date(date.getTime() - (offset*60*1000))
    setStartDate(offsetDate);
    const dateStr = offsetDate.toISOString().split('T')[0];
    getDeputyInfo(`${BACKEND_URI}/api/diputado/date/${dateStr}`);
  }

  return (
    <div>
      <Head>
        <link rel='shortcut icon' href='/favicon.png' />
        <title>#DiputadxDelDía</title>
        <meta name='viewport' content='width=device-width, initial-scale=1, user-scalable=no' />
      </Head>

      <nav id='nav' className='nav-bar'>
        <div className='app-logo'>
          <Image src={logo} alt='Diputadx del Día' />
        </div>
        <ul className='nav-items'>
          <li><a href='#top'>Principal</a></li>
          <li><a href='#attendance'>Asistencia</a></li>
          <li><a href='#expenses'>Gastos</a></li>
          <li><a href='#votes'>Votaciones</a></li>
        </ul>
        <div className={styles.changeDeputy}>
          {
            availableDates.length > 0 &&
            <DatePicker 
              className='datepicker'
              dateFormat="dd/MM/yyyy"
              selected={startDate}
              onChange={changeDeputy}
              customInput={<CustomDatePicker />}
              filterDate={isValidDate}
            />
          }
        </div>
      </nav>

      {
        loading ? 
          <div className='loading-spinner'>
            <div className='lds-facebook'>
              <div></div>
              <div></div>
              <div></div>
            </div>
          </div>
        :
        (error || datesError) ? <div>Hubo un error al cargar los datos</div>
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
