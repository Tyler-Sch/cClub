import React, { useContext, useEffect } from 'react';
import MainWindow from './main/MainWindow';
import Login from './loginPage/Login';
import RecipeList from './recipePage/RecipeList';
import { Route, Redirect } from 'react-router-dom';
// import protectedFetch from './helpers';
import { UserContext } from './stores/UserStore';
import Filter from './filters/Filter';
import GroceryList from './GroceryPage/GroceryList';


function ComingSoon() {
  return (
    <div>
      <h1 className="title">Feature Coming Soon</h1>
    </div>
  )
}



function Logoff() {
  const { setLogin, setTargetList } = useContext(UserContext);
  localStorage.removeItem('Authorization');
  setLogin(false);
  setTargetList(null);

  return (
    <Redirect to="/" />
  )
}

export default function App(props) {
  useEffect(() => {
    console.log('useEffect just fired in App');
  })

  return (
    <div>

        <h1 className="title">
          CookingClub
        </h1>
        <MainWindow />
        <Route path="/my-recipes/" component={RecipeList} />
        <Route path="/user/login/" component={Login} />
        <Route path="/grocery-list/" component={GroceryList} />
        <Route path="/user/friends/" component={ComingSoon} />
        <Route path="/search/filters/" component={Filter} />
        <Route path="/user/logoff/" component={Logoff} />
    </div>
  )
}
