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
      'searchQuery': ''
    }
    this.getNextRecipe = this.getNextRecipe.bind(this);
    this.addRecipe = this.addRecipe.bind(this);
    this.updateSearch = this.updateSearch.bind(this);
    this.search = this.search.bind(this);
  }

  componentDidMount() {
    this.fetchRandomRecipes(20);
  }

  async fetchRandomRecipes(numRecipes) {
    const response = await fetch(
      `http://localhost:5000/recipes/random/${numRecipes}`
    );

    const json = await response.json();
    const currentRecipes = this.state.recipes.slice(0, this.currentRecipe);
    console.log(currentRecipes)
    this.setState({
      'recipes': [...currentRecipes, ...json.recipes]
    });
  }

  updateSearch(e) {
    this.setState({
      'searchQuery': e.target.value
    })
  }

  async search(e) {
    // this recipe has trouble when no search results are returned.
    // should set up a tile that for such a case
    // for now, the main pic doesnt change when there is an empty search return
    // which is really annoying when you hit the end of the normal list

    if (this.state.searchQuery.trim().length === 0) {
      this.fetchRandomRecipes(20);
    } else {
      const searchParams = this.state.searchQuery.split(',').map(i => i.trim());
      const plusForSpace = searchParams.map(i => i.split(' ').join('+'));
      const joinedParams = plusForSpace.map(i => `include=${i}`).join('&');
      const url = `http://localhost:5000/recipes/filter?${joinedParams}`;
      e.preventDefault();
      const restrictedRecipes = await fetch(url);
      const json = await restrictedRecipes.json();
      if (json.length == 0) {
        return
      }
      const currentRecipes = this.state.recipes.slice(0, this.state.currentRecipe + 1);
      console.log(`current recipe length = ${currentRecipes.length}`)

      this.setState({
        'recipes': [...currentRecipes,...json],
        'currentRecipe': this.state.currentRecipe + 1
      });
    }
  }

  getNextRecipe() {
    const recipeIndex = this.state.currentRecipe;
    if (this.state.recipes.length - this.state.currentRecipe <= 2) {
      if (this.state.searchQuery == '') {
        this.fetchRandomRecipes(20);
        return
      }
      else {
        console.log('I am in search part of getNextRecipe')
        const event = document.createEvent('Event');
        this.search(event);
        return
      }

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
        <div className="level">
          <h1 className="title">Cooking Club</h1>
          <IngredientSearchBar
            update={this.updateSearch}
            val={this.state.searchQuery}
            submit={this.search}
          />
        </div>
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


const IngredientSearchBar = (props) => {
  return (
    <div className="field has-addons">
      <div className="control">
        <input onChange={props.update}
          className="input"
          type="text"
          placeholder="Separate ingredients with comma"
          value={props.val}
        />
      </div>
      <div className="control">
        <a onClick={props.submit} className="button is-info">
          Search
        </a>
      </div>
    </div>
  )
}




ReactDOM.render(
  <App />,
  document.getElementById('root')
);
