import { useSearchParams } from 'next/navigation';

// React Hooks
import { useEffect, useState, useCallback } from 'react';

// Components
import Main from '../components/Main';

export default function HomeByDate() {

  const searchParams = useSearchParams();

  const [ date, setDate ] = useState(undefined);
  const [ error, setError ] = useState(false);
	const [ errorMsg, setErrorMsg ] = useState('');
  const [ loading, setLoading ] = useState(true);

	const getParamDate = useCallback(() => {
    setLoading(true);
		setTimeout(async () => {
			let dateCandidate;
			const search = searchParams.get('date');
			// Let's check if we have a date in the URL
			if (search) {
				try {
					dateCandidate = new Date(search + ' 04:00:00');
					setDate(dateCandidate);
          setError(false);
				} catch (e) {
					console.error('Unexpected date format', e);
          setError(true);
          setErrorMsg('La fecha ingresada no es válida.');
				}
			}
      setLoading(false);
		}, 1000);
	}, [searchParams]);

	useEffect(() => {
		getParamDate();
	}, [getParamDate]);

  if (loading) {
    return (
      <div className="loader">
        <div className="lds-ripple"><div></div><div></div></div>
      </div>
    )
  } else if (error) {
    return (
      <div className="loader">
        <h1 className='error-msg'>{errorMsg} :(</h1>
      </div>
    )
  }

  return <Main date={date} />;
}
