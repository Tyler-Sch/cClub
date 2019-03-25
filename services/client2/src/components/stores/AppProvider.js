import React, { createContext, useState, useEffect } from 'react';
import { encodeData } from '../helpers';
import queryString from 'query-string';

export const AppContext = new createContext();


const foodObj = {
  'Dairy and Eggs': 100,
  'Poultry': 500,
  'Sausage and Lunch Meat': 700,
  'Pork': 1000,
  'Nuts and Seeds': 1200,
  'Beef': 1300,
  'Finfish and Shellfish': 1500,
  'Lamb, Veal, and Game': 1700
}


export default function AppContextWrapper(props) {
  const [recipes, setRecipe] = useState([]);
  const [currentRecipe, setCurrent] = useState(0);
  const [filters, setFilters] = useState([]);
  const [filterObj, setFilterObj] = useState(foodObj);
  const numRecipesToFetch = 5;
  const recipeUrlPrefix = "http://localhost:5000/"

  // checks if recipe list is running out and fetches more if they are
  useEffect(() => {
    if ((recipes.length - currentRecipe) <= 2) {
      console.log('fetching');
      if (filters.length > 0){
        fetchFilteredRecipes(numRecipesToFetch);
      }
      else {
        fetchRandomRecipes(numRecipesToFetch);
      }
    }
  })

  // get random recipes
  const fetchRandomRecipes = async (numRecipes) => {
    const encodedQueryString = queryString.stringify({'filter':filters})
    const url = recipeUrlPrefix + `recipes/random/${numRecipes}?${encodedQueryString}`;
    const response = await fetch(
      url
    );
    const data = await response.json();
    setRecipe([...recipes,...data.recipes])
    // console.log(data);
  }
  
  const fetchFilteredRecipes = async (numRecipes) => {
    const encodedQueryString = queryString.stringify({'filter':filters})
    const url = recipeUrlPrefix + `recipes/random/${numRecipes}?${encodedQueryString}`
    // console.log(url);
    const response = await fetch(url);
    const data = await response.json();
    // console.log(data);
    setRecipe([...recipes, ...data.recipes])

  }

  const resetRecipes = () => {
    const slicedRecipes = recipes.slice(0, currentRecipe + 1);
    setRecipe(slicedRecipes);
  }

  return (
    <AppContext.Provider value={{
      targetRecipe: recipes[currentRecipe],
      changeRecipe: setCurrent,
      currentRecipe,
      filterObj,
      filters,
      setFilters,
      resetRecipes

    }} >
      { props.children }
    </AppContext.Provider>
  )
}
