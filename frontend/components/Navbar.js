import React, { forwardRef, useState, useCallback, useEffect } from 'react';

// Date Picker
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { getData, BACKEND_URL } from '../utils/utils';

const MyDatePicker = forwardRef(({ value, onClick }, ref) => (
  <button className="custom-datepicker-button" onClick={onClick} ref={ref}>
    <b>Fecha: </b> 
    {
      new Date(value.replace('/','-').replace('/','-').split('-').reverse().join('-')+' 04:00:00').toLocaleDateString("es-ES", {
        day: "numeric",
        month: "long",
      })
    }
  </button>
));
MyDatePicker.displayName = 'MyDatePicker';

const CustomDatePicker = ({pageDate}) => {

  const [ availableDates, setAvailableDates ] = useState([]);
  const [ startDate, setStartDate ] = useState(pageDate);
  const [ datesError, setDatesError ] = useState(false);

  const isValidDate = (date) => {
    return availableDates.filter((d) => d.toISOString().split('T')[0] === date.toISOString().split('T')[0]).length > 0;
  };

  const changeDeputy = (date) => {
    const dateISOString = date.toISOString().split('T')[0];
    window.location.href = "/archivo/diputado?fecha=" + dateISOString;
  }

  const getAvailableDates = useCallback(() => {
    setTimeout(async () => {
      const jsonData = await getData(`${BACKEND_URL}/dates`);
      if (!jsonData) {
        setDatesError(true);
      } else {
        setDatesError(false);
        const data = jsonData.dates.map((date) => new Date(date));
        setAvailableDates(data);
        setStartDate(pageDate)
      }
    }, 1000);
  }, [setDatesError, setAvailableDates]);

  useEffect(() => {
    getAvailableDates();
  }, [getAvailableDates]);

  if (availableDates.length === 0 || datesError) {
    return (
      <>
        <b>Fecha:</b> ---
      </>
    )
  } else {
    return (
      <DatePicker 
        className='datepicker'
        dateFormat="dd/MM/yyyy"
        selected={startDate}
        onChange={changeDeputy}
        customInput={<MyDatePicker />}
        filterDate={isValidDate}
      />
    )
  }
}

const Navbar = ({date}) => {

  const showMobileMenu = () => {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
      x.className += " responsive";
    } else {
      x.className = "topnav";
    }
  }

  const closeMenu = () => {
    var x = document.getElementById("myTopnav");
    if (x.className !== "topnav") {
      x.className = "topnav";
    }
  }

  return (
    <div className="navbar-container">
      <nav className="topnav" id="myTopnav">
        <a href="#" className='logo-container' onClick={closeMenu}>
          <img src="/logo.png" alt="Logo" className='app-logo'/>
        </a>
        <a href="#attendance" onClick={closeMenu}>Asistencia</a>
        <a href="#expenses" onClick={closeMenu}>Gastos</a>
        <a href="#votings" onClick={closeMenu}>Votaciones</a>
        <a href="#about" onClick={closeMenu}>Método de Elección</a>
        <a><CustomDatePicker pageDate={date}/></a>
        <a className="icon" onClick={showMobileMenu}>
          <i className="fa fa-bars"></i>
        </a>
      </nav>
    </div>
  )
}

export default Navbar