import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Link, withRouter, Redirect } from 'react-router-dom';
import 'bulma';
import App from './components/App';


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
