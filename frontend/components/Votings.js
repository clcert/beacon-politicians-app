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
        vote.vote_option === 'Afirmativo' ?
          <div className={styles.greenVote}><b>{ vote.vote_option }</b></div>
          :
        vote.vote_option === 'En Contra' ?
          <div className={styles.redVote}><b>{ vote.vote_option }</b></div>
          :
          <div><b>{ vote.vote_option }</b></div>
      }
      <div className={styles.link}>
        <a href={`https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion=${vote.voting_id}`} target='_blank' rel="noreferrer">
          <button>
            Ver detalle
          </button>
        </a>
      </div>
    </div>
  )
}

export default Votings