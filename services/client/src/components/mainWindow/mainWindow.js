import React from 'react';


const ButtonMain = (props) => {
  return (
    <button onClick={props.handleClick}>{props.name}</button>
  )
}

const MainWindow = (props) => {
  return (
        <section className="box">
          <div className="columns">
            <div className="column is-one-fifth">
              <ButtonMain name='Add to recipe list' handleClick={props.addRecipe} />
            </div>
            <div className="column">
              {props.children}
            </div>
            <div className="column is-one-fifth">
              <ButtonMain name="Next Please" handleClick={props.next} />
            </div>
          </div>
          <nav className="breadcrumb is-centered">
            <ul>
              <li className="is-active"><a href="#">Recipe List</a></li>
              <li><a href="#">Grocery List</a></li>
              <li><a href="#">Friends</a></li>
              <li><a href="#">Filters</a></li>
            </ul>
          </nav>
        </section>
  )

}

export default MainWindow
