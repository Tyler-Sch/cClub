import React, { useState, useEffect } from 'react';

export default function RecipeList(props) {
  const [recipeLists, setRecipeList] = useState([]);

  const currentRecipeList = props.currentRecipes.map((i) => (
    <li key={i.id}><a href={i.url} target="_blank">{i.name}</a></li>
    )
  );

  console.log(props)
  // should come up with a better way of centering info.
  // currently it's in an h1 tag
  return (
    <div className="section">
      <h1 className="has-text-centered">
        {!props.loggedIn &&
        <span className="tag is-warning ">please log in to save recipes</span>
        }
        <h1 className="title">Recipes</h1>

      <ul>
        {currentRecipeList}
      </ul>

      {
        props.currentRecipes.length > 0 && props.loggedIn &&
        <button className="button is-dark is-small is-hover">Save recipe list</button>
      }
    </h1>
    </div>
  )
}
