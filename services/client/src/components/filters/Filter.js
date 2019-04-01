import React, { useContext } from 'react';
import { AppContext } from '../stores/AppProvider';

export default function Filter() {

  const {
    filters,
    setFilters,
    filterObj,
    resetRecipes } = useContext(AppContext);

  const addToFilterList = (id) => {
    if (filters.includes(id)) {
      const targetIndex = filters.indexOf(id);
      const filter = [...filters]
      filter.splice(targetIndex, 1)
      setFilters(filter);
    }
    else {
      setFilters([...filters, id])
    }
  }

  const filterHtml = Object.keys(filterObj).map((k) => (
    <div className="field">
      <lable className="checkbox">
        <input
          type="checkbox"
          checked={filters.includes(filterObj[k])}
          onClick={() => addToFilterList(filterObj[k])}
         />
       {k}
      </lable>
    </div>
  ))

  return (
    <div className="box">
      <h1 className="title">Items to exclude</h1>
      {filterHtml}
      <div className="field">
        <lable className='submit'>
          <button
            type="submit"
            className="button is-primary"
            onClick={() => resetRecipes() }
          >
          Exclude these items
        </button>

        </lable>
      </div>
    </div>
  )
}
