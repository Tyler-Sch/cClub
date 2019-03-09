import React, { useState, useEffect } from 'react';
import MainWindow from './main/MainWindow';
import Login from './Login';
import RecipeList from './RecipeList';
import { Route } from 'react-router-dom';
import protectedFetch from './helpers';



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
  const [firstLoad, setFirstLoad] = useState(true);
  const numRecipesToFetch = 5;
  const userUrlPrefix = "http://localhost:5003/";
  const recipeUrlPrefix = "http://localhost:5000/"


  useEffect(() => {
    // fetch starting recipes
    if (firstLoad){
    // fetchRandomRecipes(numRecipesToFetch);
    if (localStorage.getItem('Authorization') !== null) {
      // test if login token still ok and renew
      checkLoggedIn();
    }
    fetchRecipeLists();
    }

    setFirstLoad(false);
  })

  const checkLoggedIn = async () => {
    console.log('checking for login')
    const url = userUrlPrefix + 'users/check-login';
    console.log(url);
    const response = await protectedFetch(url, 'GET');
    if (response.loggedIn === true) {
      console.log("user is logged in");
      setLogin(true);
      localStorage.setItem('Authorization', response.token);
    }
  }


  // const fetchRandomRecipes = async (numRecipes) => {
  //   const url = recipeUrlPrefix + `recipes/random/${numRecipes}`;
  //   console.log(url);
  //   const response = await fetch(
  //     url
  //   );
  //   const data = await response.json();
  //   setRecipe([...recipes,...data.recipes])
  // }
  //
  // const cycleRecipes = () => {
  //   // fetches new recipes when needed
  //   setCurrent(currentRecipe + 1);
  //   if(currentRecipe + 2 === recipes.length) {
  //     fetchRandomRecipes(numRecipesToFetch);
  //   }
  // }

  const addRecipe = () => {
    if (!userRecipes.includes(recipes[currentRecipe])) {
      setUserRecipes([...userRecipes, recipes[currentRecipe]]);
      console.log(userRecipes);
    }
  }
  const fetchRecipeLists = async () => {
    const url = userUrlPrefix + 'users/get-recipeLists';
    const response = await protectedFetch(url,'GET')
    if (response.recipeList != undefined){
      setUserRecipeList(response.recipeList);
    }
  }


  return (
    <div>

        <h1 className="title">
          CookingClub
        </h1>
        <MainWindow
          addToRecipeList={addRecipe}
          loggedIn={loggedIn}
        />
        <Route path="/my-recipes/"
          render={(props) => <RecipeList
                                currentRecipes={userRecipes}
                                loggedIn={loggedIn}
                                fetchRecipeLists={fetchRecipeLists}
                                recipelists={userRecipeList}
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
