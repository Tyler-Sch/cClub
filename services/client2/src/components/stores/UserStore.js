import React, { createContext, useState, useContext } from 'react';
import { AppContext } from './AppProvider';
import protectedFetch from '../helpers';

export const UserContext = new createContext();

export default function User(props) {
  const [userRecipes, setUserRecipes] = useState([]);
  const [userRecipeList, setUserRecipeList] = useState([]);
  const [loggedIn, setLogin] = useState(false);
  const userUrlPrefix = "http://localhost:5003/";


  const fetchRecipeLists = async () => {
    const url = userUrlPrefix + 'users/get-recipeLists';
    const response = await protectedFetch(url,'GET')
    if (response.recipeList != undefined){
      setUserRecipeList(response.recipeList);
    }
  }

  // const App = useContext(AppContext);
  const addRecipe = (recipeToAdd) => {
    if (!userRecipes.includes(recipeToAdd)) {
      setUserRecipes([...userRecipes, recipeToAdd]);
      console.log(userRecipes);
    }
  }

  return (
    <UserContext.Provider value={{
        loggedIn,
        userRecipes,
        userRecipeList,
        setUserRecipes,
        addRecipe,
        fetchRecipeLists,
        userUrlPrefix
      }} >
      {props.children}
    </UserContext.Provider>
  );
}
