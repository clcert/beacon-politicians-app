import { useSearchParams } from 'next/navigation';

// React Hooks
import { useEffect, useState, useCallback } from 'react';

// Components
import DeputyOverview from '../components/DeputyOverview';
import DeputyAttendance from '../components/DeputyAttendance';
import ExpensesSummary from '../components/expenses/ExpensesSummary';
import OperationalDistribuition from '../components/expenses/OperationalDistribuition';
import HistoryMonths from '../components/expenses/HistoryMonths';
import DeputyVotings from '../components/DeputyVotings';
import About from '../components/About';
import Navbar from '../components/Navbar';

import { BACKEND_URL, getData } from '../utils/utils';

export default function Home() {

  const searchParams = useSearchParams();

	const [ paramDate, setParamDate ] = useState(undefined);
  const [ date, setDate ] = useState(new Date());
  const [ deputyData, setDeputyData] = useState({});
  const [ loading, setLoading ] = useState(true);
  const [ error, setError ] = useState(true);
	const [ errorMsg, setErrorMsg ] = useState('');

	const getParamDate = useCallback(() => {
		setLoading(true);
		setTimeout(async () => {
			let dateCandidate = undefined;
			const search = searchParams.get('date');
			// Let's check if we have a date in the URL
			if (search !== null) {
				try {
					dateCandidate = new Date(search + ' 04:00:00');
					setParamDate(dateCandidate);
				} catch (e) {
					console.error('Unexpected date format', e);
				}
			}
		}, 1000);
	}, [searchParams]);
		

	const getDate = useCallback(() => {
		setLoading(true);
    setTimeout(async () => {
			let dateCandidate = undefined;
			const jsonData = await getData(`${BACKEND_URL}/api/dates`);
			if (jsonData !== null) {
				const dates = jsonData.dates;
				const lastDate = dates[dates.length - 1];
				dateCandidate = new Date(lastDate);
			}
			// If we still don't have a date, raise an error
			if (dateCandidate === undefined) {
				setErrorMsg('No hay datos disponibles para la fecha solicitada.');
				setError(true);
			} else {
				setDate(dateCandidate);
				setError(false);
			}
    }, 1000);
  }, [setError, setDate]);

	const getDeputyData = useCallback(() => {
		setLoading(true);
		setTimeout(async () => {
			const localDateStr = date.toLocaleDateString("es-ES", {day: "2-digit", month: "2-digit", year: "numeric", timeZone: "America/Santiago"})
			const formattedDate = localDateStr.replace('/', '-').replace('/', '-').split('-').reverse().join('-');
			const jsonData = await getData(`${BACKEND_URL}/api/diputado/date/${formattedDate}`);
			if (jsonData !== null) {
				setDeputyData(jsonData);
			} else {
				setErrorMsg('No hay datos disponibles para la fecha solicitada.');
				setError(true);
			}
			setLoading(false);
		}, 1000);
	}, [date, error, setError, setDeputyData, setLoading]);

	useEffect(() => {
		getParamDate();
	}, [getParamDate]);

	useEffect(() => {
		if (paramDate !== undefined) {
			setError(false)
			setDate(paramDate);
		} else {
			getDate();
		}
	}, [paramDate]);

  useEffect(() => {
		if (!error) {
			getDeputyData();
		}
  }, [date]);

  if (loading) {
    return (
      <div className="loader">
				<div className="lds-ripple"><div></div><div></div></div>
			</div>
    )
  } else if (error || !deputyData) {
		return (
			<div className="loader">
				<h1 className='error-msg'>{errorMsg} :(</h1>
			</div>
		)
	} else {
		return (
			<div>
				<Navbar date={date} />
				<div id="header">
					<DeputyOverview data={ deputyData }/>
				</div>

				<div id="main">
					<header className="major container medium">
						<h4>
							Escogid{ deputyData.termination } el { deputyData.date } (horario UTC) en base al Pulso&nbsp;
							<a href={`https://random.uchile.cl/beacon/2.0-beta1/chain/1/pulse/${ deputyData.record }`} target='_blank' rel="noreferrer">
								#{ deputyData.record }
							</a>{' '}
							del faro de aleatoriedad de Random UChile.
						</h4>
						<p className='verification-text'>
							Comprueba la elección utilizando nuestro script (Python)&nbsp;
							<a href='https://github.com/clcert/beacon-politicians-app' target='_blank' rel="noreferrer">
								disponible en GitHub
							</a>.
						</p>
					</header>

					<div id="attendance" className="box container">
						<header>
							<h2>Asistencia</h2>
						</header>
						<section className="feature left">
							<DeputyAttendance data={deputyData }/>
						</section>
					</div>

					<div id="expenses" className="box container">
						<header>
							<h2>Dieta Parlamentaria y Asignaciones { deputyData.sex == '1' ? 'del diputado' : 'de la diputada'}</h2>
						</header>
						<section className="feature right">
							<ExpensesSummary data={deputyData} />
						</section>
						<section className="feature left">
							<OperationalDistribuition data={deputyData} />
						</section>
						<section className="feature right">
							<HistoryMonths data={deputyData} />
						</section>
					</div>

					<div id="votings" className="box container">
						<DeputyVotings data={deputyData} />
					</div>

					<footer id="about" className="major container medium">
						<About />
					</footer>

				</div>

				<div id="footer">
					<div className="container medium">
						<header>
							<h2>Referencias</h2>
								<ol >
									<li id='ref-1'>
										Cálculo hecho según justificaciones a inasistencias, para más información visitar: <br />
										<a href='https://opendata.camara.cl/camaradiputados/WServices/WSSala.asmx' target='_blank' rel='noreferrer'>
											https://opendata.camara.cl/camaradiputados/WServices/WSSala.asmx
										</a>.
									</li>
									<li id='ref-2'>
										Documento que acredita la dieta parlamentaria desde agosto 2022:<br />
										<a href='https://www.camara.cl/transparencia/doc/dieta_actualizada.pdf' target='_blank' rel='noreferrer'>
											https://www.camara.cl/transparencia/doc/dieta_actualizada.pdf
										</a>.
									</li>
									<li id='ref-3'>
										Los datos acerca de los gastos operacionales fueron obtenidos desde:<br />
										<a href={`https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx?prmId=${deputyData.deputy_id}`} target='_blank' rel='noreferrer'>
											{`https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx?prmId=${deputyData.deputy_id}`}
										</a>.
									</li>
									<li id='ref-4'>
										Los datos acerca de los gastos en oficinas parlamentarias fueron obtenidos desde:<br />
										<a href='https://www.camara.cl/transparencia/oficinasparlamentarias.aspx' target='_blank' rel='noreferrer'>
											https://www.camara.cl/transparencia/oficinasparlamentarias.aspx
										</a>.
									</li>
									<li id='ref-5'>
										Los datos acerca de los gastos de personal de apoyo fueron obtenidos desde:<br />
										<a href='https://www.camara.cl/transparencia/personalapoyogral.aspx' target='_blank' rel='noreferrer'>
											https://www.camara.cl/transparencia/personalapoyogral.aspx
										</a>.
									</li>
									<li id='ref-6'>
										Existen desfases con respecto a los meses con gastos declarados en cada categoría.
									</li>
								</ol>
						</header>

						<header className="major last">
							<h2>¿Dudas o comentarios?</h2>
						</header>

						<p>Contáctanos al mail <b>random[arroba]uchile.cl</b></p>

						<ul className="icons">
							<li><a href="https://twitter.com/randomuchile" className="icon brands fa-twitter"><span className="label">Twitter</span></a></li>
							<li><a href="https://github.com/clcert/beacon-politicians-app" className="icon brands fa-github"><span className="label">Github</span></a></li>
							<li><a href="https://t.me/DiputadxDelDia" className="icon brands fa-telegram"><span className="label">Telegram</span></a></li>
						</ul>

						<ul className="copyright">
							<li>Diseño: <a href="http://html5up.net">&copy; Directive, HTML5 UP</a>, template adaptado.</li>
						</ul>

					</div>
				</div>
			</div>
		);
	}
}
