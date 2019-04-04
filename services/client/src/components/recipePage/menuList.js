import React from 'react';
import Dropdown from '../standardComps/Dropdown';

export default function MenuList(props) {

  return (
    <div>
      <Dropdown text='Lists'>
        <div className="dropdown-item">
          <div className="menu">
            <p className="menu-label">Create new list</p>
            <ul className="menu-list">
              <li>
                <form className="field" onSubmit={props.submit}>
                  <div className="control">
                    <input
                      size="7"
                      type="text"
                      placeholder="new list name"
                      onChange={props.change}
                      value={props.val}
                    />
                  </div>
                </form>
              </li>
            </ul>
            <p className="menu-label">ListName</p>
            <ul className="menu-list">
              {
                (props.userRecipeL.length > 0) && props.userRecipeL.map((i, idx) => (
                  <li key={idx} onClick={() => props.setTargetList(idx)}><a>
                  {i.listName}</a></li>
                ))
              }

            </ul>
          </div>
        </div>
      </Dropdown>
    </div>
  )
}
