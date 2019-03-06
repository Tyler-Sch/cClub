import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Link, withRouter, Redirect } from 'react-router-dom';
import 'bulma';
import App from './components/App';


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


function AppRouter() {
  return (
    <BrowserRouter>
      <div>
        <Route path="/" component={App} />


      </div>
    </BrowserRouter>
  );
}


ReactDOM.render(<AppRouter />, document.getElementById('root'));
