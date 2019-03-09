import React, { useContext } from 'react';
import PictureWindow from './PictureWindow';
import Nav from './Nav';
import { AppContext } from '../stores/AppProvider';
import { UserContext } from '../stores/UserStore';

export default function MainWindow(props) {
  const { changeRecipe, targetRecipe, currentRecipe } = useContext(AppContext);
  const { setUserRecipes, userRecipes, addRecipe } = useContext(UserContext);

  return (
    <section className="box">
      <div className="columns">
        <div className="column is-one-fifth">
          <button onClick={() => addRecipe(targetRecipe)}>Add this recipe</button>
        </div>
        <div className="column">
          {
          (targetRecipe !== undefined)
          ? <PictureWindow recipe={targetRecipe} />
        : <div>Loading</div>
          }
        </div>
        <div className="column is-one-fifth">
          <button onClick={() => changeRecipe(currentRecipe + 1)}>Next Recipe</button>
        </div>
      </div>
      <Nav loggedIn={props.loggedIn} />
    </section>
  );
}
