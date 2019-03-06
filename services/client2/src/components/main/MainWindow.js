import React from 'react';
import PictureWindow from './PictureWindow';
import Nav from './Nav';

export default function MainWindow(props) {
  // console.log(props)
  return (
    <section className="box">
      <div className="columns">
        <div className="column is-one-fifth">
          <button onClick={props.addToRecipeList}>Add this recipe</button>
        </div>
        <div className="column">
          {
          (props.recipe !== undefined)
          ? <PictureWindow recipe={props.recipe} />
        : <div>Loading</div>
          }
        </div>
        <div className="column is-one-fifth">
          <button onClick={props.nextRecipe}>Next Recipe</button>
        </div>
      </div>
      <Nav loggedIn={props.loggedIn} />
    </section>
  );
}
