import React, { useEffect } from 'react';

const Navbar = () => {

  const showMobileMenu = () => {
    var x = document.getElementById("myTopnav");
    console.log(x);
    if (x.className === "topnav") {
      x.className += " responsive";
    } else {
      x.className = "topnav";
    }
  }

  return (
    <div className="navbar-container">
      <nav className="topnav" id="myTopnav">
        <a href="#" className='logo-container'>
          <img src="/logo.png" alt="Logo" className='app-logo'/>
        </a>
        <a href="#attendance">Asistencia</a>
        <a href="#expenses">Gastos</a>
        <a href="#votings">Votaciones</a>
        <a href="#about">Método de Elección</a>
        <a href="#about">Choose</a>
        <a className="icon" onClick={e=>showMobileMenu()}>
          <i className="fa fa-bars"></i>
        </a>
      </nav>
    </div>
  )
}

export default Navbar