import React, { useContext, useState, useEffect, useRef } from 'react';
import protectedFetch from './helpers';
import Dropdown from './standardComps/Dropdown';
import { UserContext } from './stores/UserStore';


export default function RecipeList(props) {

  const [newListName, setNewListName] = useState('');
  const {
    userRecipes,
    fetchRecipeLists,
    userRecipeList,
    userUrlPrefix,
    loggedIn } = useContext(UserContext);

  

  const createRecipeList = async (e) => {
    // need to fix hardcoded url
    e.preventDefault();
    const data = {
      recipeListName: newListName,
      recipes: []
    }
    const url = userUrlPrefix + 'users/create-new-recipe-list';
    console.log(data);
    const responseData = await protectedFetch(url, 'POST', data);
    console.log(responseData);
    setNewListName('');
    fetchRecipeLists();
  }

  const currentRecipeList = userRecipes.map((i) => (
    <li key={i.id}><a href={i.url} target="_blank">{i.name}</a></li>
    )
  );

  // should come up with a better way of centering info.
  // currently it's in an h1 tag which feel oh so wrong
  return (
    <div className="section">
      <Dropdown text='Lists'>
        <div className="dropdown-item">
          <div className="menu">
            <p className="menu-label">Create new list</p>
            <ul className="menu-list">
              <li>
                <form className="field" onSubmit={createRecipeList}>
                  <div className="control">
                    <input
                      size="7"
                      type="text"
                      placeholder=" new list name"
                      onChange={(e) => setNewListName(e.target.value)}
                      value={newListName}
                    />
                  </div>
                </form>
              </li>
            </ul>
            <p className="menu-label">ListName</p>
            <ul className="menu-list">
              {
                (userRecipeList.length > 0) && userRecipeList.map((i, idx) => (
                  <li key={idx}>{i.listName}</li>
                ))
              }

            </ul>
          </div>
        </div>
      </Dropdown>
      <h1 className="has-text-centered">
        {!loggedIn &&
        <span className="tag is-warning ">please log in to save recipes</span>
        }
        <h1 className="title">Recipes</h1>

      <ul>
        {currentRecipeList}
      </ul>

      {
        userRecipes.length > 0 && loggedIn &&
        <button className="button is-dark is-small is-hover">Save recipe list</button>
      }
    </h1>
    </div>
  )
}
