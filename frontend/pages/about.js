import React from 'react'
import Head from 'next/head'
import Link from 'next/link'

import styles from '../styles/About.module.css'

const about = () => {
  return (
    <div>
      <nav id='nav'>
        <ul>
          <li><Link href='/'>Volver</Link></li>
        </ul>
      </nav>
      <Head>
        <link rel='shortcut icon' href='/favicon.png' />
        <title>#DiputadxDelDía - ¿Cómo funciona?</title>
        <meta name='viewport' content='width=device-width, initial-scale=1, user-scalable=no' />
      </Head>
      <article className={styles.aboutSection}>
        <div className={styles.boxContainer}>
          <h1>¿Cómo funciona #DiputadoDelDia?</h1>
          <p>
            Cada día a las 00:00 (hora de Chile continental) la aplicación #DiputadoDelDía escoje, 
            aleatoriamente, un número entre 1 y 155 (relacionando cada número con uno de los 155 
            diputados en ejercicio actualmente). Luego de esto, recolecta y despliega información 
            pública del diputado escogido proporcionada por la página oficial de la Cámara de Diputados.
          </p>
        </div>
        <div className={styles.boxContainer}>
          <h2>¿Cómo se escoge aleatoriamente al #DiputadoDelDía?</h2>
          <p>
            Para escojer un número de manera aleatoria entre 1 y 155, #DiputadoDelDía extrae, el 
            último valor generado por el Faro de Aleatoriedad de la Universidad de Chile (<a href='https://random.uchile.cl' target='_blank'>https://random.uchile.cl</a>). 
            Ese valor (512 bits aleatorios) es utilizado como 'semilla' para correr un proceso 'pseudo-aleatorio' 
            que tiene como finalidad escoger un número, al azar, entre 1 y 155.
          </p>
        </div>
        <div className={styles.boxContainer}>
          <h2>¿Semilla? ¿Pseudo-aleatorio? ¿Qué significa eso?</h2>
          <p>
          Ningún sistema computacional puede escoger un número realmente aleatorio. Lo que pueden hacer es escoger un número 'pseudo-aleatoriamente'. Esto consiste en que si se tiene un valor inicial (denominado 'semilla') lo bastantemente impredecible (en términos matemáticos, que posee una alta entropía), entonces el número escogido también sera bastantemente impredecible (para todos los efectos prácticos, escogido al azar).
          </p>
        </div>
        <br/>
      </article>
      <article id='contact' className='wrapper style4'>
        <div className='container medium'>
          <footer>
            <p>
              Para más información sobre como verificar la selección del #DiputadoDelDia 
              dirígete a nuestro repositorio de Github: <a href='https://github.com/clcert/beacon-politicians-app'>https://github.com/clcert/beacon-politicians-app</a>
            </p>
            <br />
            <ul id='copyright'>
              <li>&copy;Design: <a href='http://html5up.net'>HTML5 UP</a></li>
            </ul>
          </footer>
        </div>
      </article>
    </div>
  )
}

export default about