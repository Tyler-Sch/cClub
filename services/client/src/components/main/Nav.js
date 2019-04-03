import React from 'react';
import { Link } from 'react-router-dom';

export default function Nav(props) {


  return (
    <nav className="is-centered breadcrumb">
      <ul>
        <li>
          <Link to="/my-recipes/">Recipe List</Link>
        </li>
        <li><Link to="/grocery-list/">Grocery List</Link></li>
        <li><Link to="/user/friends/">Friends</Link></li>
        <li><Link to="/search/filters/">Filters</Link></li>
        {
          (props.loggedIn)
          ? <li><Link to="/user/logoff/">Log off</Link></li>
          :  <li><Link to="/user/login/">Login</Link></li>
        }
      </ul>
    </nav>
  )
}
