import React, { useState, useEffect } from 'react';

export default function RecipeList(props) {


  const currentRecipeList = props.currentRecipes.map((i) => (
    <li key={i.id}><a href={i.url} target="_blank">{i.name}</a></li>
    )
  );

  // should come up with a better way of centering info.
  // currently it's in an h1 tag
  return (
    <div className="section">
      <h1 className="has-text-centered">
        <h1 className="title">Recipes</h1>
      <ul>
        {currentRecipeList}
      </ul>
    </h1>
    </div>
  )
}
