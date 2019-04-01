import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Link, withRouter, Redirect } from 'react-router-dom';
import 'bulma';
import App from './components/App';
import User from './components/stores/UserStore';
import AppContextWrapper from './components/stores/AppProvider';

function AppRouter() {
  console.log('index firing')
  return (
    <User>
      <AppContextWrapper>
        <BrowserRouter>
          <div>
            <Route path="/" component={App} />
          </div>
        </BrowserRouter>
      </AppContextWrapper>
    </User>
  );
}


ReactDOM.render(<AppRouter />, document.getElementById('root'));
