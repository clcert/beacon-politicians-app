import React from 'react';

const DeputyVotings = ({voting, gender}) => {
  const isMale = gender === 'MALE';

  return (
    <>
      <header>
        <h2>Últimas Votaciones</h2>
        <p>Se listan las { voting.length } votaciones en sala más recientes.</p>
      </header>
      { 
        voting.map((vote, index) => {
          return (
            <SingleVote key={index} vote={vote} isMale={isMale} />
          )
        })
      }
    </>
  )
}

const SingleVote = ({vote, isMale}) => {
  const votingDate = new Date(vote.voting_date);
  const dateStr = votingDate.toLocaleDateString('es-ES', {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "America/Santiago"
  });
  const articleTitle = vote.document_title.replaceAll('&quot;', '"')
  const articleTitleAsTxt = articleTitle.split("\n").filter((content) => content!== '').map((item, key) => {
    return <span key={key}>{item}<br/></span>
  });
  const bulletinUrl = `https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion=${vote.voting_id}`

  return (
    <div className='vote-container'>
      <div className='head'>
        <h3><a href={ bulletinUrl } target='_blank'>{ vote.bulletin_number }</a></h3>
        <div className='date'><i>{ dateStr }</i></div>
      </div>
      
      <div className='matters'>{ articleTitleAsTxt }</div>
      { 
        vote.article_text !== '' && 
        vote.article_text !== 'No se encontró el artículo' && 
        <p className='article-text'>{vote.article_text}</p>
      }
      <div className='outcome-info'>
        <div className='deputy-vote-text'>
          <span className='vote'>
            {
              isMale ?
                'El diputado '
                :
                'La diputada '
            }
          </span>
          {
            vote.voted === 'Afirmativo' ?
              <span className='vote green-vote'>votó a favor</span>
              :
            vote.voted === 'En Contra' ?
              <span className='vote red-vote'>votó en contra</span>
              :
              <span className='vote'>se abstuvo</span>
          }
        </div>
        <div className='more-info'>
          <div className='votes-info'>
            <b style={{'color': 'gray'}}>Resultado Votación</b>
            <br/>
            <b style={{'color': 'limegreen'}}>{ vote.total_approved }</b> &nbsp;
            <b style={{'color': 'red'}}>{ vote.total_rejected }</b> &nbsp;
            <b style={{'color': 'gray'}}>{ vote.total_abstention }</b>&nbsp;
            <br/>
            {
              vote.result === 'Aprobado' ?
                <b className='vote-count green-vote'>Aprobado</b>
                :
              vote.result === 'Unánime' ?
                <b className='vote-count red-vote'>Rechazado</b>
                :
                <b className='vote-count'>{ vote.result }</b>
            }
          </div>
        </div>
      </div>
    </div>
  )
}

export default DeputyVotings