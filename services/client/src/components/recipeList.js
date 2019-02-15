import React from 'react';


const RecipeList = (props) => {
  const items = props.recipes.map(i =>
    <li key={i.name}><a href={i.url}
        target="_blank">{i.name}</a></li>
  );
  return (
      <div classNmae="content is-large">
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
