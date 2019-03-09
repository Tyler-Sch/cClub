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
    <AppContextWrapper>
       <User>
        <BrowserRouter>
          <div>
            <Route path="/" component={App} />
          </div>
        </BrowserRouter>
      </User>
    </AppContextWrapper>
  );
}


ReactDOM.render(<AppRouter />, document.getElementById('root'));
