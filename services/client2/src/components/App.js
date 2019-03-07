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
  const [userRecipes,setUserRecipes] = useState([]);
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
    console.log(recipes);
    console.log(currentRecipe);
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
