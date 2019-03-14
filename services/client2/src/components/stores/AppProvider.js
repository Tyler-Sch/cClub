import React, { createContext, useState, useEffect } from 'react';

export const AppContext = new createContext();

export default function AppContextWrapper(props) {
  const [recipes, setRecipe] = useState([]);
  const [currentRecipe, setCurrent] = useState(0);
  const numRecipesToFetch = 5;
  const recipeUrlPrefix = "http://localhost:5000/"

  useEffect(() => {
    if ((recipes.length - currentRecipe) <= 2) {
      console.log('fetching recipes from AppProvider');
      fetchRandomRecipes(numRecipesToFetch);
    }
  })

  const fetchRandomRecipes = async (numRecipes) => {
    const url = recipeUrlPrefix + `recipes/random/${numRecipes}`;
    const response = await fetch(
      url
    );
    const data = await response.json();
    setRecipe([...recipes,...data.recipes])
  }

  const getRecipesFromIds = (listOfIds) => {
    const x = 2;
  }

  return (
    <AppContext.Provider value={{
      targetRecipe: recipes[currentRecipe],
      changeRecipe: setCurrent,
      currentRecipe
    }} >
      { props.children }
    </AppContext.Provider>
  )
}
