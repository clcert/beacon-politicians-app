import React from 'react'

const About = () => {
  return (
    <>
      <h2>Preguntas Frecuentes</h2>
      <h3>¿Cómo funciona #DiputadoDelDia?</h3>
      <p>
        Cada día a las 00:01 (hora de Chile continental) la aplicación #DiputadoDelDía escoje, 
        aleatoriamente, un número entre 1 y 155 (relacionando cada número con uno de los 155 
        diputados en ejercicio actualmente). Luego de esto, recolecta y despliega información 
        pública del diputado escogido proporcionada por la página oficial de la Cámara de Diputados.
      </p>
      <h3>¿Cómo se escoge aleatoriamente al #DiputadoDelDía?</h3>
      <p>
        Para escojer un número de manera aleatoria entre 1 y 155, #DiputadoDelDía extrae, el 
        último valor generado por el Faro de Aleatoriedad de la Universidad de Chile (<a href='https://random.uchile.cl' target='_blank' rel='noreferrer'>https://random.uchile.cl</a>). 
        Ese valor (512 bits aleatorios) es utilizado como &quot;semilla&quot; para correr un proceso &quot;pseudo-aleatorio&quot; 
        que tiene como finalidad escoger un número, al azar, entre 1 y 155.
      </p>
      <h3>¿Semilla? ¿Pseudo-aleatorio? ¿Qué significa eso?</h3>
      <p>
        Ningún sistema computacional puede escoger un número realmente aleatorio. Lo que 
        pueden hacer es escoger un número &quot;pseudo-aleatoriamente&quot;. Esto consiste 
        en que si se tiene un valor inicial (denominado &quot;semilla&quot;) lo bastantemente 
        impredecible (en términos matemáticos, que posee una alta entropía), entonces el 
        número escogido también sera bastantemente impredecible (para todos los efectos 
        prácticos, escogido al azar).
      </p>
    </>
  )
}

export default About