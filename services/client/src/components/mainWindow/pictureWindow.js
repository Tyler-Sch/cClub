import React from 'react';

const PictureWindow = ({ recipe: { name, pic_url, source, url } }) => {
  return (
    <div>
      <h1 className="has-text-centered title">{name}</h1>
      <a className="title"
          href={url}
          target="_blank">
      {pic_url !== 'missing'
      ? <img style={{marginLeft: 'auto',
                     marginRight: 'auto',
                     display: 'block',
                     objectFit: 'cover',
                     height: '400px',
                     width: '400px',
                     paddingBottom:'1em'
                   }}
       src={pic_url}  />
      : <img style={{marginLeft: 'auto',
                     marginRight: 'auto',
                     display: 'block',

                   }}
      src="https://via.placeholder.com/400x400.png?text=No+Picture" />
      }
      </a>
      <h6 className="subtitle has-text-centered">{source}</h6>
    </div>
  )
}

export default PictureWindow;
