import React from 'react';
import styles from '../styles/home/Votings.module.css';

const Votings = ({deputyInfo}) => {
  return (
    <div className='container'>
      <header>
        <h2>Votaciones</h2>
        <p>Se listan las votaciones en sala más recientes.</p>
      </header>
      <div className='row'>
        <div className={styles.table}>
          { 
            deputyInfo.voting.map((vote, index) => {
              return <SingleVote key={index} vote={vote} />
            })
          }
        </div>
      </div>
    </div>
  )
}

const SingleVote = ({vote}) => {
  return (
    <div className={styles.voteContainer}>
      <div className={styles.head}>
        <h3>{ vote.description }</h3>
        <div className={styles.date}><i>{ vote.date }</i></div>
      </div>
      
      <div className={styles.matters}>{ vote.name }</div>
      { 
        vote.article !== '' && 
        vote.article !== 'No se encontró el artículo' && 
        <p>{vote.article}</p>
      }
      {
        vote.vote_option === 'Afirmativo' ?
          <div className='vote green-vote'>{ vote.vote_option }</div>
          :
        vote.vote_option === 'En Contra' ?
          <div className='vote red-vote'>{ vote.vote_option }</div>
          :
          <div className='vote'>{ vote.vote_option }</div>
      }
      <div className={styles.moreInfo}>
        <div className={styles.votesInfo}>
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
        <div className={styles.linkInfo}>
          <a href={`https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion=${vote.voting_id}`} target='_blank' rel="noreferrer">
            Ver detalle
          </a>
        </div>
      </div>
    </div>
  )
}

export default Votings