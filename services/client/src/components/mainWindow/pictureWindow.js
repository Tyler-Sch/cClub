import React from 'react';

const PictureWindow = ({ recipe: { name, pic_url, source, url } }) => {
  return (
    <div>
      <h1 className="has-text-centered"><a className="title"
          href={url}
          target="_blank">{name}</a></h1>
      {pic_url !== 'missing'
      ? <img style={{marginLeft: 'auto',
                     marginRight: 'auto',
                     display: 'block'}}
       src={pic_url} height="400px" width="400px" />
      : <img style={{marginLeft: 'auto',
                     marginRight: 'auto',
                     display: 'block'}}
      src="https://via.placeholder.com/400x400.png?text=No+Picture" />
      }
      <h6 className="subtitle has-text-centered">{source}</h6>
    </div>
  )
}

export default PictureWindow;
