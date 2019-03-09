import React, { createContext, useState } from 'react';

export const UserContext = new createContext();

export default function User(props) {
  const [loggedIn, setLogin] = useState(false);
  const [userNumber, setUserNumber] = useState(0);
  const [userName, setUserName] = useState('potato');

  return (
    <UserContext.Provider value={{ loggedIn, userNumber, userName, setUserName }} >
      {props.children}
    </UserContext.Provider>
  );
}
