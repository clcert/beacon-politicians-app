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
      <div className="loader">Cargando</div>
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
					<h3>Get shady with science</h3>
					<p>Vitae natoque dictum etiam semper magnis enim feugiat amet curabitur tempor orci penatibus. Tellus erat mauris ipsum fermentum etiam vivamus.</p>
					<ul className="actions special">
						<li><a href="#" className="button">Join our crew</a></li>
					</ul>
				</footer>

			</div>

			<div id="footer">
				<div className="container medium">

					<header className="major last">
						<h2>Questions or comments?</h2>
					</header>

					<p>Vitae natoque dictum etiam semper magnis enim feugiat amet curabitur tempor
					orci penatibus. Tellus erat mauris ipsum fermentum etiam vivamus.</p>

					<form method="post" action="#">
						<div className="row">
							<div className="col-6 col-12-mobilep">
								<input type="text" name="name" placeholder="Name" />
							</div>
							<div className="col-6 col-12-mobilep">
								<input type="email" name="email" placeholder="Email" />
							</div>
							<div className="col-12">
								<textarea name="message" placeholder="Message" rows="6"></textarea>
							</div>
							<div className="col-12">
								<ul className="actions special">
									<li><input type="submit" value="Send Message" /></li>
								</ul>
							</div>
						</div>
					</form>

					<ul className="icons">
						<li><a href="#" className="icon brands fa-twitter"><span className="label">Twitter</span></a></li>
						<li><a href="#" className="icon brands fa-facebook-f"><span className="label">Facebook</span></a></li>
						<li><a href="#" className="icon brands fa-instagram"><span className="label">Instagram</span></a></li>
						<li><a href="#" className="icon brands fa-github"><span className="label">Github</span></a></li>
						<li><a href="#" className="icon brands fa-dribbble"><span className="label">Dribbble</span></a></li>
					</ul>

					<ul className="copyright">
						<li>&copy; Untitled. All rights reserved.</li><li>Design: <a href="http://html5up.net">HTML5 UP</a></li>
					</ul>

				</div>
			</div>
    </div>
  )
}
