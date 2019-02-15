import React from 'react';


const RecipeList = (props) => {
  const items = props.recipes.map(i =>
    <li><a href={i.url}
        target="_blank">{i.name}</a></li>
  );
  return (
      <ul>
        {items}
      </ul>
  )
}

export default RecipeList;
