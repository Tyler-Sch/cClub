import React, { useEffect, createContext, useState, useContext, useLayoutEffect } from 'react';
// import { AppContext } from './AppProvider';
import protectedFetch from '../helpers';

export const UserContext = new createContext();

export default function User(props) {
  const [userRecipes, setUserRecipes] = useState([]);
  const [userRecipeList, setUserRecipeList] = useState([]);
  const [loggedIn, setLogin] = useState(null);
  const userUrlPrefix = "http://localhost:5003/";

  useEffect(() => {
    // check on loading
    checkLogin();
  }, [])


  const checkLogin = async () => {

    console.log('firing checkLogin');
    console.log(`logged in is currenctly ${loggedIn}`)
    const token = localStorage.getItem('Authorization');
    if (token) {
      // check validity
      console.log("token is not null")
      const url = userUrlPrefix + 'users/check-login';
      const response = await protectedFetch(url, 'GET');
      console.log(response);
      if (response.loggedIn == true) {
        console.log('setting login to true');
        setLogin(true);
      }
      else {
        setLogin(false);
      }
    }
    else {setLogin(false);}
  }

  useEffect(() => {
    if (loggedIn === true) {
      console.log('fetching recipes');
      console.log(`loggedIn is ${loggedIn}`)
      fetchRecipeLists();
    }
  }, [loggedIn])

  const fetchRecipeLists = async () => {
    console.log('fetching recipes');
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
        setLogin,
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
