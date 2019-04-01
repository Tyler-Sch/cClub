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

  const sortRecipeListIngredients = (a, b) => {
    if (a.ingredient >  b.ingredient) {
      return 1;
    }
    if (a.ingredient == b.ingredient) {
      return 0;
    }
    if (a.ingredient < b.ingredient) {
      return -1;
    }

  }

  const getDisplayItemsNames = () => {
    const listItems = [...recipeListIngredients];
    listItems.sort((a, b) => sortRecipeListIngredients(a, b))
    if (displayItemName) {
      const justItems = listItems.map(i => i.ingredient);
      console.log(justItems);
      const filteredItems = justItems.filter((v, i, a) => a.indexOf(v) === i);
      console.log(filteredItems);
      const display = filteredItems.map(i => <li>{i}</li>);
      return display;
    }
    else {
      const display = listItems.map(i => <li>{i.original_text}</li>)
      return display;
    }

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
