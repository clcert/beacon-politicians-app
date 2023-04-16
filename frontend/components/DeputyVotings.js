import React from 'react';

const DeputyVotings = ({data}) => {
  return (
    <>
      <header>
        <h2>Últimas Votaciones</h2>
        <p>Se listan las votaciones en sala más recientes.</p>
      </header>
      { 
        data.voting.map((vote, index) => {
          return (
            <section key={index}>
              <header>
                <h3>{ vote.description }</h3>
                <p>{ vote.name }</p>
              </header>
              { 
                vote.article !== '' && 
                vote.article !== 'No se encontró el artículo' && 
                <p>{vote.article}</p>
              }
            </section>
          )
        })
      }
    </>
  )
}

export default DeputyVotings