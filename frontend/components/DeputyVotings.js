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
            <SingleVote key={index} vote={vote} sex={data.sex} />
            // <section key={index}>
            //   <header>
            //     <h3>{ vote.description }</h3>
            //     <p>{ vote.name }</p>
            //   </header>
            //   { 
            //     vote.article !== '' && 
            //     vote.article !== 'No se encontró el artículo' && 
            //     <p>{vote.article}</p>
            //   }
            // </section>
          )
        })
      }
    </>
  )
}

const SingleVote = ({vote, sex}) => {
  return (
    <div className='vote-container'>
      <div className='head'>
        <h3>{ vote.description }</h3>
        <div className='date'><i>{ vote.date }</i></div>
      </div>
      
      <div className='matters'>{ vote.name }</div>
      { 
        vote.article !== '' && 
        vote.article !== 'No se encontró el artículo' && 
        <p>{vote.article}</p>
      }
      <span className='vote'>
        {
          sex === '0' ?
            'La diputada votó '
            :
            'El diputado votó '
        }
      </span>
      {
        vote.vote_option === 'Afirmativo' ?
          <span className='vote green-vote'>{ vote.vote_option }</span>
          :
        vote.vote_option === 'En Contra' ?
          <span className='vote red-vote'>{ vote.vote_option }</span>
          :
          <span className='vote'>{ vote.vote_option }</span>
      }
      <div className='more-info'>
        <div className='votes-info'>
          <b style={{'color': 'gray'}}>Resultado Votación</b>
          <br/>
          <b style={{'color': 'limegreen'}}>{ vote.total_yes }</b> &nbsp;
          <b style={{'color': 'red'}}>{ vote.total_no }</b> &nbsp;
          <b style={{'color': 'gray'}}>{ vote.total_abstention }</b>&nbsp;
          <br/>
          {
            vote.result === 'Aprobado' ?
              <b className='vote-count green-vote'>{ vote.result }</b>
              :
            vote.result === 'Unánime' ?
              <b className='vote-count red-vote'>{ vote.result }</b>
              :
              <b className='vote-count'>{ vote.result }</b>
          }
        </div>
        <div className='link-info'>
          <a href={`https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion=${vote.voting_id}`} target='_blank' rel="noreferrer">
            Ver detalle
          </a>
        </div>
      </div>
    </div>
  )
}

export default DeputyVotings