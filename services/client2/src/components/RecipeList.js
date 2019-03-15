import React, { useContext, useState, useEffect, useRef } from 'react';
import protectedFetch from './helpers';
import Dropdown from './standardComps/Dropdown';
import { UserContext } from './stores/UserStore';


export default function RecipeList(props) {

  const [newListName, setNewListName] = useState('');
  const [targetList, setTargetList] = useState(null);
  const [lenRecipeList, setLenRecipeList] = useState(null);

  const {
    userRecipes,
    setUserRecipes,
    fetchRecipeLists,
    userRecipeList,
    setUserRecipeList,
    userUrlPrefix,
    loggedIn,
    savedRecipes,
    setSavedRecipes } = useContext(UserContext);

  // when target list changes, render that new list
  useEffect(() => {
    if (targetList !== null) {
      console.log('firing useEffect changing from targetlist')
      setSavedRecipes(userRecipeList[targetList].recipes)
    }
  }, [targetList])

  // when new list is created, put new list in target in focus
  useEffect(() => {
    if (lenRecipeList === null && userRecipeList.length >= 0) {
      setLenRecipeList(userRecipeList.length);
    }
    else if (userRecipeList.length > lenRecipeList) {
      setTargetList(0);
      setLenRecipeList(userRecipeList.length);
      setSavedRecipes([]);
    }
  }, [userRecipeList])

  // add a new recipe list
  const createRecipeList = async (e) => {
    e.preventDefault();
    const recipeData = userRecipes;
    const data = {
      recipeListName: newListName,
      recipes: {}
    }
    const url = userUrlPrefix + 'users/create-new-recipe-list';
    const responseData = await protectedFetch(url, 'POST', data);
    setNewListName('');
    fetchRecipeLists();
  }

  // save unsaved recipes to database
  const saveRecipeList = async () => {
    const data = {
        'targetListId': userRecipeList[targetList].listId[0],
        'recipes': userRecipes
    }
    const url = userUrlPrefix + 'users/add-recipes-to-list';
    const response = await protectedFetch(url, 'POST', data);
    if (response.status === 'success') {
        setSavedRecipes([...userRecipes, ...savedRecipes]);
        setUserRecipes([]);
        // fetching all the recipe lists is ineffcient, but hey,
        // we dont want to do premature optimization, right???
        fetchRecipeLists();
    }
    else {
        console.log('error in saveRecipeList in RecipeList');
    }
  }

  // delete saved recipe from database
  const removeSavedRecipe = async (id) => {
    const url = userUrlPrefix + 'users/remove-recipe';
    const data = {
      'targetList': userRecipeList[targetList].listId[0],
      'targetRecipe': id
    }
    const response = await protectedFetch(url, 'POST', data);
    if (response.status === 'success') {
      setSavedRecipes(response.updatedRecipes);
      fetchRecipeLists();
    }
    else {
      console.log("there was an error in removeSavedRecipe in RecipeList")
    }
  }

  // remove unsaved item from recipe list
  const removeElement = (id) => {
    setUserRecipes(userRecipes.filter((i) => i.id !== id));
  }



  const currentRecipeList = userRecipes.map((i) => (
    <li className="" key={i.id}>
      <div className="">
        <a className="has-text-grey" href={i.url} target="_blank">{i.name}</a>
        <button onClick={() => removeElement(i.id)}className="delete is-pulled-right"></button>
      </div>
    </li>
    )
  );

  const savedRecipeList = savedRecipes.map((i) => (
    <li key={i.id}>
      <div>
        <a className="has-text-dark" href={i.url} target="_blank">{i.name}</a>
        <button onClick={() => removeSavedRecipe(i.id)}
          className="delete is-pulled-right"></button>
      </div>
    </li>
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
                      placeholder="new list name"
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
                  <li key={idx} onClick={() => setTargetList(idx)}>{i.listName}</li>
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
        <h1 className="title">{
            (targetList !== null)
            ? userRecipeList[targetList].listName
            : 'Recipes'}
        </h1>

      <ul>
        {currentRecipeList}
        {savedRecipeList}
      </ul>

      {
        userRecipes.length > 0 && loggedIn &&
        <button onClick={() => saveRecipeList()} className="button is-dark is-small is-hover">Save recipe list</button>
      }
    </h1>
    </div>
  )
}
