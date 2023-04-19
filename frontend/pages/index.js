// React Hooks
import { useEffect, useState, useCallback } from 'react';

import { BACKEND_URL, getData } from '../utils/utils';
import Main from '../components/Main';

export default function Home() {

  const [ loading, setLoading ] = useState(true);
  const [ date, setDate ] = useState(new Date());		

	const getDate = useCallback(() => {
    setLoading(true);
    setTimeout(async () => {
			let dateCandidate;
			const jsonData = await getData(`${BACKEND_URL}/api/dates`);
			if (jsonData) {
				const dates = jsonData.dates;
				const lastDate = dates[dates.length - 1];
				dateCandidate = new Date(lastDate);
			}
			// If we still don't have a date, raise an error
			if (dateCandidate) {
				setDate(dateCandidate);
			}
      setLoading(false);
    }, 1000);
  }, [setDate]);

	useEffect(() => {
		getDate();
	}, [getDate]);

  if (loading) {
    return (
      <div className="loader">
        <div className="lds-ripple"><div></div><div></div></div>
      </div>
    )
  }

	return <Main date={date} />;
}
