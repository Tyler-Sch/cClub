import React, { useContext, useEffect, useState } from 'react';
import { UserContext } from './stores/UserStore';
import { AppContext } from './stores/AppProvider';
import protectedFetch from './helpers';

export default function GroceryList() {
  const [recipeListIngredients, setRecipeListIngredients] = useState([]);
  const [shouldAddCurrentRecipes, setShouldAddCurrentRecipes] = useState(false);
  const [displayItemName, setDisplayItemName] = useState(true);
  const { fetchIngredients } = useContext(AppContext);
  const {
    savedRecipes,
    userRecipes,
  } = useContext(UserContext);

  useEffect(() => {
    const recipeIds = [...savedRecipes,...userRecipes].map((i) => i.id);
    // console.log(recipeIds);
    fetchWrapper(recipeIds);
  }, [userRecipes])

  const fetchWrapper = async (recipeIds) => {
    const data = await fetchIngredients(recipeIds.map(i => parseInt(i)));
    setRecipeListIngredients(data);
    console.log('fetched data for grocery list')
  }

  const getDisplayItemsNames = () => {

    const display = displayItemName
                    ? recipeListIngredients.map(i => (
                      <li>{i.ingredient}</li>
                    ))
                    : recipeListIngredients.map(i => (
                      <li>{i.original_text}</li>
                    ))
    console.log(displayItemName)


    return display;
  }
  const getDisplayItemsOriginalText = () => {
    const ogText = recipeListIngredients.map(i => (
      <li>{i.original_text}</li>
    ));
    return ogText;
  }

  // console.log(recipeListIngredients)
  return (
    <div>
      <div className="level">
        <div className="level-left">
          <h1 className='title'>Grocery List</h1>
        </div>
        <div className="level-right">
          <button
            className="button"
            onClick={() => setShouldAddCurrentRecipes(!shouldAddCurrentRecipes)}
          >
            Add recipes from current list
          </button>
          <button className="button"
                  onClick={() => setDisplayItemName(!displayItemName)}
            >
            switch to recipe amount view
          </button>
        </div>
      </div>

      <ul>
        {
          recipeListIngredients.length >= 1 && shouldAddCurrentRecipes && getDisplayItemsNames()
        }
      </ul>
    </div>
  )
}
