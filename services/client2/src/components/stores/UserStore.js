import React, { useEffect, createContext, useState, useContext, useLayoutEffect } from 'react';
// import { AppContext } from './AppProvider';
import protectedFetch from '../helpers';

export const UserContext = new createContext();

export default function User(props) {
  const [userRecipes, setUserRecipes] = useState([]);
  const [userRecipeList, setUserRecipeList] = useState([]);
  const [savedRecipes, setSavedRecipes] = useState([]);
  const [loggedIn, setLogin] = useState(null);
  const userUrlPrefix = "http://localhost:5003/";

  useEffect(() => {
    // check on loading
    checkLogin();
  }, [])


  // check if previous login token exists and if it's valid
  const checkLogin = async () => {
    const token = localStorage.getItem('Authorization');
    if (token) {
      // check validity
      const url = userUrlPrefix + 'users/check-login';
      const response = await protectedFetch(url, 'GET');
      if (response.loggedIn == true) {
        setLogin(true);
      }
      else {
        setLogin(false);
      }
    }
    else {setLogin(false);}
  }


  // fetch recipe lists if loggedIn changes to true
  useEffect(() => {
    if (loggedIn === true) {
      fetchRecipeLists();
    }
  }, [loggedIn])

  // async function that fetches user's recipe lists
  const fetchRecipeLists = async () => {
    const url = userUrlPrefix + 'users/get-recipeLists';
    const response = await protectedFetch(url,'GET')
    if (response.recipeList != undefined){
      setUserRecipeList(response.recipeList.reverse());
    }
  }

  // add recipes to unsaved list
  const addRecipe = (recipeToAdd) => {
    if (![...userRecipes, ...savedRecipes].includes(recipeToAdd)) {
      setUserRecipes([...userRecipes, recipeToAdd]);
    }
  }

  return (
    <UserContext.Provider value={{
        loggedIn,
        setLogin,
        userRecipes,
        userRecipeList,
        setUserRecipes,
        addRecipe,
        fetchRecipeLists,
        userUrlPrefix,
        savedRecipes,
        setSavedRecipes,
      }} >
      {props.children}
    </UserContext.Provider>
  );
}
