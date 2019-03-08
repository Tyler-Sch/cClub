import React, { useState, useEffect } from 'react';
import MainWindow from './main/MainWindow';
import Login from './Login';
import RecipeList from './RecipeList';
import { Route } from 'react-router-dom';

function ComingSoon() {
  return (
    <div>
      <h1 className="title">Feature Coming Soon</h1>
    </div>
  )
}


export default function App(props) {
  const [recipes, setRecipe] = useState([]);
  const [currentRecipe, setCurrent] = useState(0);
  const [loggedIn, setLogin] = useState(false);
  const [userRecipes, setUserRecipes] = useState([]);
  const [userRecipeList, setUserRecipeList] = useState([]);
  const numRecipesToFetch = 5;


  useEffect(() => {
    // fetch starting recipes
    if (recipes.length < numRecipesToFetch){
    console.log('firing fetch random recipes');
    const new_recipes = fetchRandomRecipes(numRecipesToFetch);
    }

  })

  const fetchRandomRecipes = async (numRecipes) => {
    const response = await fetch(
      `http://localhost:5000/recipes/random/${numRecipes}`
    );
    const data = await response.json();
    setRecipe([...recipes,...data.recipes])
  }

  const cycleRecipes = () => {
    // fetches new recipes when needed
    setCurrent(currentRecipe + 1);
    if(currentRecipe + 2 === recipes.length) {
      fetchRandomRecipes(numRecipesToFetch);
    }
  }

  const addRecipe = () => {
    if (!userRecipes.includes(recipes[currentRecipe])) {
      setUserRecipes([...userRecipes, recipes[currentRecipe]])
    }
  }
  const fetchRecipeLists = async () => {
    console.log('Trying to fetch recipes');
    const response = await ProtectedFetch(
      'http://localhost:5003/users/get-recipeLists',
      'GET'
    )
    setUserRecipeList(response.recipeList);
    console.log(userRecipeList);
  }

  const ProtectedFetch = async (url, method, data = {}) => {
    const response = await fetch(
      url,
      {
        method: method,
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          "Authorization": localStorage.getItem('Authorization')
        },
        body: null
      }
    )
    const response_data = await response.json();
    // think I need something to catch an error here
    return response_data
  }

  return (
    <div>
      <h1 className="title">
        CookingClub
      </h1>
      <MainWindow
        addToRecipeList={addRecipe}
        nextRecipe={cycleRecipes}
        recipe={recipes[currentRecipe]}
        loggedIn={loggedIn}
      />
      <Route path="/my-recipes/"
        render={(props) => <RecipeList
                              currentRecipes={userRecipes}
                              loggedIn={loggedIn}
                              fetchRecipeLists={fetchRecipeLists}
                            />}

                            />
      <Route path="/user/login/"
        render={(props) => <Login switchLogin={() => setLogin(true)}/>} />
      <Route path="/grocery-list/" component={ComingSoon} />
      <Route path="/user/friends/" component={ComingSoon} />
      <Route path="/search/filters/" component={ComingSoon} />
    </div>
  )
}
