import React, { createContext, useState, useContext } from 'react';
import { AppContext } from './AppProvider';

export const UserContext = new createContext();

export default function User(props) {
  const [userRecipes, setUserRecipes] = useState([]);
  const [userRecipeList, setUserRecipeList] = useState([]);
  const [loggedIn, setLogin] = useState(false);
  const userUrlPrefix = "http://localhost:5003/";


  const App = useContext(AppContext);


  return (
    <UserContext.Provider value={{ loggedIn }} >
      {props.children}
    </UserContext.Provider>
  );
}
