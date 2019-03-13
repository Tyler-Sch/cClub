import React, { useState, useContext } from 'react';
import { Redirect } from 'react-router-dom';
import { UserContext } from './stores/UserStore';


function Login(props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [inCreateNew, setCreateNew] = useState(false);
  const [redirect, setRedirect] = useState(false);

  const { setLogin } = useContext(UserContext);

  const sub = async (e) => {
    e.preventDefault();
    console.log('loggin in')
    const url = (inCreateNew) ? 'http://localhost:5003/users/create-new' :
    'http://localhost:5003/users/login';
    // const url = (inCreateNew) ? process.env.REACT_APP_CREATE_NEW_USER :
    // process.env.REACT_APP_LOGIN;
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
    // check if login success before saving token
    if (data.loggedIn) {
      const token = data.token;
      localStorage.setItem('Authorization', token);
      setRedirect(true);
      setLogin(true);
      // props.switchLogin();
    }
    // handle error
    else {
      alert(data.message);
    }
  }
  if (!redirect) {
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
  else {
    return (
    <Redirect to="/" />
    )
  }
}

export default Login;
