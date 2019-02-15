import React from 'react';
import ReactDOM from 'react-dom';
import 'bulma';
import MainWindow from './components/mainWindow/mainWindow';
import PictureWindow from './components/mainWindow/pictureWindow';
import RecipeList from './components/recipeList';


class App extends React.Component {
  constructor(props) {
    super();
    this.state = {
      'recipes': [],
      'currentRecipe': 0,
      'userRecipes': [],
    }
    this.getNextRecipe = this.getNextRecipe.bind(this);
    this.addRecipe = this.addRecipe.bind(this);
  }

  componentDidMount() {
    this.fetchRandomRecipes(20);
  }

  async fetchRandomRecipes(numRecipes) {
    const response = await fetch(
      `http://localhost:5000/recipes/random/${numRecipes}`
    );

    const json = await response.json();
    console.log(json);
    const currentRecipes = this.state.recipes.slice(0, this.currentRecipe);
    this.setState({
      'recipes': [...currentRecipes, ...json.recipes]
    });
    console.log(this.state.recipes);
  }



  getNextRecipe() {
    const recipeIndex = this.state.currentRecipe;
    if (this.state.recipes.length - this.state.currentRecipe == 2) {
      this.fetchRandomRecipes(20);
    }
    this.setState({
      'currentRecipe': recipeIndex + 1
    });
  }
  addRecipe() {
    const recipeList = this.state.userRecipes;
    const currentRecipe = this.state.recipes[this.state.currentRecipe];
    if (!recipeList.includes(currentRecipe)){
      this.setState({
        'userRecipes': [...recipeList, currentRecipe]
      })
    }
  }

  render() {
    const recipeIndex = this.state.currentRecipe;
    return (
      <div>
        <h1 className="title">Cooking Club</h1>
        <div className="section">
          <MainWindow addRecipe={this.addRecipe} next={this.getNextRecipe}>
            {
              this.state.recipes.length > 0
              ? <PictureWindow recipe={this.state.recipes[recipeIndex]} />
              : <h1> loading </h1>
            }
          </MainWindow>
        </div>
        <div className="section">
          <RecipeList recipes={this.state.userRecipes} />
        </div>
      </div>
    )
  }
}







ReactDOM.render(
  <App />,
  document.getElementById('root')
);
