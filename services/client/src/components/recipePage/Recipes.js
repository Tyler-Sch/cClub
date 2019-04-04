import React from 'react';

export default function Recipes(props) {
  return (
    <div>
    {props.listItems.map((i, idx) => (
      <li key={i.id}>
        <div>
          <a
            className={`${props.classColor}`}
            href={i.url}
            target="_blank"
          >
            {i.name}
          </a>
          <button
            onClick={() => props.onClickFunction(i.id)}
            className="delete is-pulled-right"
          ></button>
        </div>
      </li>
    ))}
  </div>
  )
}
