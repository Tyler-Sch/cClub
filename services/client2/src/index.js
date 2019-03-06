import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Link } from 'react-router-dom';
import 'bulma';


class App extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div>
        <h1 className="title">Cooking Club</h1>

      </div>
    );
  }
}

const Example = () => {
  const [count, setCount] = useState(0);
  useEffect(() => {
    document.title = `You clicked ${count} times`;
  });
  return (
    <div>
      <p>You clicked {count} times </p>
      <button onClick={() => setCount(count +1 )}>
      Click me!
      </button>
    </div>
  );
}

function WriteName() {
  const [username, setUsername] = useState(null);
  const [currentVal, setVal] = useState(null);
  return (

    <div>
      <p> enter your name here</p>
      <p>{username}</p>
      <input type="text" placeholder="name here"
        onChange={(e) => setVal(e.target.value)}/>
      <input type="submit" onClick={(e) => {
        setUsername(currentVal);
      }} />
    </div>
  )
}

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [inCreateNew, setCreateNew] = useState(false);

  const sub = async (e) => {
    e.preventDefault();
    console.log('loggin in')
    const url = (inCreateNew) ? 'http://localhost:5003/users/create-new' :
    'http://localhost:5003/users/login';
    console.log(url);
    console.log({username, password, email})

    const response = await fetch(
      url,
      {
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': JSON.stringify({ username, password, email })
      }
    );
    const data = await response.json();
    console.log(data);


  }

  return(
    <div className="section">
      <div className="container">
        <div className="box">
          <form
            onSubmit={(e) => sub(e)}>
            <div className="field">
              <label className="label">User</label>
              <div className="control">
                <input className="input is-focused" type="text"
                 value={username}
                 onChange={(e) => setUsername(e.target.value)}
                 />
              </div>
            </div>
            <div className="field">
              <label className="label">Password</label>
              <div className="control">
                <input className="input" type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>
            { (inCreateNew)
              ? (<div className="field">
                <label className="label">Email</label>
                <div className="control">
                  <input className="input" type="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  />
                </div>
              </div>)
                : <div></div>
              }

            <div className="field">
              <div className="control">
                <button className="button" type="submit">
                  {
                  (!inCreateNew)
                  ? <div>Login</div>
                  : <div>Create User</div>
                  }
                </button>
              </div>
            </div>
          </form>
          {
            (!inCreateNew)
            ? (<div>
                <a onClick={(e) => setCreateNew(true)}>create new user </a>
              </div>)
            :
            <div></div>
          }
        </div>
      </div>
    </div>
  )
}

function CreateUser() {
  return (
    <h1>In the create user page</h1>
  )
}

function AppRouter() {
  return (
    <BrowserRouter>
      <div>
        <Route path="/" component={App} />
        <Route path="/my-recipes/" component={Example} />
        <Route path="/user/login/" component={Login} />
        <Route path="/users/create-new/" component={Login} />
      </div>
    </BrowserRouter>
  );
}


ReactDOM.render(<AppRouter />, document.getElementById('root'));
