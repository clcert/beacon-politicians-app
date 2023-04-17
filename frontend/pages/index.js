import { useSearchParams } from 'next/navigation';

// React Hooks
import { useEffect, useState } from 'react';

// Components
import DeputyOverview from '../components/DeputyOverview';
import DeputyAttendance from '../components/DeputyAttendance';
import ExpensesSummary from '../components/expenses/ExpensesSummary';
import OperationalDistribuition from '../components/expenses/OperationalDistribuition';
import HistoryMonths from '../components/expenses/HistoryMonths';
import DeputyVotings from '../components/DeputyVotings';
import About from '../components/About';

const BACKEND_URL = 'http://127.0.0.1:5000';

function getLastDeputyData() {
  const url = `${BACKEND_URL}/api/diputadodeldia`;
  return fetch(url)
    .then((res) => {
      if (res.status === 200) {
        return res.json();
      }
      return null;
    })
    .catch(() => {
      return null;
    });
}

export default function Home() {

  const searchParams = useSearchParams();
  const search = searchParams.get('date');

  const [ date, setDate ] = useState(new Date());
  const [ deputyData, setDeputyData] = useState({});
  const [ loading, setLoading ] = useState(true);
  const [ error, setError ] = useState(false);

  useEffect(() => {
    console.log('search', search);

    setLoading(true);
    setTimeout(async () => {
      const jsonData = await getLastDeputyData();
      if (jsonData === null) {
        setError(true);
      } else {
        setError(false);
        console.log('jsonData', jsonData);
        setDeputyData(jsonData);
      }
      setLoading(false);
    }, 1000);
  }, [search]);

  if (loading) {
    return (
      <div className="loader">
				<div className="lds-ripple"><div></div><div></div></div>
			</div>
    )
  }

  return (
    <div>      
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

				<div className="box alt container">
					<section className="feature left">
						<DeputyAttendance data={deputyData }/>
					</section>
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

				<div className="box container">
					<DeputyVotings data={deputyData} />
				</div>

				<footer className="major container medium">
					<About />
				</footer>

			</div>

			<div id="footer">
				<div className="container medium">
					<header>
						<h2>Referencias</h2>
							<ol >
								<li id='ref-attendance'>
									Cálculo hecho según justificaciones a inasistencias, para más información visitar: <br />
									<a href='https://opendata.camara.cl/camaradiputados/WServices/WSSala.asmx' target='_blank' rel='noreferrer'>
										https://opendata.camara.cl/camaradiputados/WServices/WSSala.asmx
									</a>.
								</li>
								<li id='op-expenses'>
									Los datos acerca de los gastos operacionales fueron obtenidos desde:<br />
									<a href={`https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx?prmId=${deputyData.deputy_id}`} target='_blank' rel='noreferrer'>
										{`https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx?prmId=${deputyData.deputy_id}`}
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
  )
}
