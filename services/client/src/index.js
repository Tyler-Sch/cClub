import React from 'react';
import ReactDOM from 'react-dom';
import 'bulma';

const PictureWindow = ({ recipe: { name, pic_url, source } }) => {
  return (
    <div>
      <h1 className="title has-text-centered"> {name}</h1>
      {pic_url !== 'missing'
      ? <img style={{marginLeft: 'auto',
                     marginRight: 'auto',
                     display: 'block'}}
       src={pic_url} height="400px" width="400px" />
      : <img style={{marginLeft: 'auto',
                     marginRight: 'auto',
                     display: 'block'}}
      src="https://via.placeholder.com/400x400.png?text=No+Picture" />
      }
      <h6 className="subtitle has-text-centered">{source}</h6>
    </div>
  )
}


class App extends React.Component {
  constructor(props) {
    super();
    this.state = {
      'recipes': [],
      'currentRecipe': 0
    }
    this.getNextRecipe = this.getNextRecipe.bind(this);
  }

  componentDidMount() {
    this.fetchRandomRecipes();
  }

  async fetchRandomRecipes() {
    const response = await fetch('http://localhost:5000/recipes/random/20');
    const json = await response.json();

    this.setState({
      'recipes': json.recipes,
    });
  }

  getNextRecipe() {
    const recipeIndex = this.state.currentRecipe;
    this.setState({
      'currentRecipe': recipeIndex + 1
    });
    console.log(this.state.currentRecipe);
  }

  render() {
    const recipeIndex = this.state.currentRecipe;
    return (
      <div>
        <h1 className="title">Cooking Club</h1>
        <div className="section">
          <MainWindow handleClick={this.getNextRecipe}>
            {
              this.state.recipes.length > 0
              ? <PictureWindow recipe={this.state.recipes[recipeIndex]} />
              : <h1> loading </h1>
            }

          </MainWindow>
        </div>
      </div>
    )
  }
}
const ButtonMain = (props) => {
  return (
    <button onClick={props.handleClick}>{props.name}</button>
  )
}

const MainWindow = (props) => {
  return (
        <section className="box">
          <div className="columns">
            <div className="column is-one-fifth box">
              <ButtonMain name='Add to recipe list' handleClick={props.handleClick} />
            </div>
            <div className="column">
              {props.children}
            </div>
            <div className="column is-one-fifth box">
              <ButtonMain name="Next Please" handleClick={props.handleClick} />
            </div>
          </div>
        </section>
  )

}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
