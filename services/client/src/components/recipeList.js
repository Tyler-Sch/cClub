import React from 'react';


const RecipeList = ({ recipes }) => {
  const items = recipes.map(i =>
    <li key={i.name}>
      <a href={i.url}
        target="_blank">{i.name}</a>
      <button className='tag delete'></button>
    </li>
  );
  return (
      <div className="">
      <h1 className="has-text-centered">
        <h1 className="is-large">Selected Recipes</h1>
          <ul>
            {items}
          </ul>
        </h1>
      </div>
  )
}

export default RecipeList;
