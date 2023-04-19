import React, { useEffect } from 'react';

const Navbar = () => {

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
        <a href="#about" onClick={closeMenu}>Choose</a>
        <a className="icon" onClick={showMobileMenu}>
          <i className="fa fa-bars"></i>
        </a>
      </nav>
    </div>
  )
}

export default Navbar