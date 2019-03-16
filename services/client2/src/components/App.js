import React, { useState, useEffect, useContext } from 'react';
import MainWindow from './main/MainWindow';
import Login from './Login';
import RecipeList from './RecipeList';
import { Route, Redirect } from 'react-router-dom';
import protectedFetch from './helpers';
import { UserContext } from './stores/UserStore';



function ComingSoon() {
  return (
    <div>
      <h1 className="title">Feature Coming Soon</h1>
    </div>
  )
}



function Logoff() {
  const { setLogin } = useContext(UserContext);
  localStorage.removeItem('Authorization');
  setLogin(false);

  return (
    <Redirect to="/" />
  )
}

export default function App(props) {


  return (
    <div>

        <h1 className="title">
          CookingClub
        </h1>
        <MainWindow

        />
      <Route path="/my-recipes/" component={RecipeList}
        />
        <Route path="/user/login/"
          render={(props) => <Login />} />
        <Route path="/grocery-list/" component={ComingSoon} />
        <Route path="/user/friends/" component={ComingSoon} />
        <Route path="/search/filters/" component={ComingSoon} />
        <Route path="/users/logoff/" component={Logoff} />
    </div>
  )
}
