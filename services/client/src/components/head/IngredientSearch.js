import React from 'react';

const IngredientSearchBar = ({ val, update, submit }) => {
  return (
    <div className="field has-addons">
      <div className="control">
        <input onChange={update}
          className="input"
          type="text"
          placeholder="Separate ingredients with comma"
          value={val}
        />
      </div>
      <div className="control">
        <a onClick={submit} className="button is-info">
          Search
        </a>
      </div>
    </div>
  )
}

export default IngredientSearchBar;
