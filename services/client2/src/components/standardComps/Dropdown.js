import React, { useState } from 'react';

export default function Dropdown(props) {
    // takes props.text for name of button and accepts child arguments
    // each should be wrapped with <div className="dropdown-item">
  const [dropdown, setToggle] = useState('')
  const toggleDropdown = () =>{
    if (dropdown !== "is-active") {
      setToggle('is-active');
    }
    else {
      setToggle('');
    }
  }
  return (
    <div className={["dropdown", dropdown].join(' ')}>
      <div className="dropdown-trigger">
        <button className="button" onClick={toggleDropdown} >
          <span>{props.text}</span>
        </button>
      </div>
      <div className="dropdown-menu" id="dropdown-menu6">
        <div className="dropdown-content">
          {props.children}
        </div>
      </div>
    </div>
  )
}
