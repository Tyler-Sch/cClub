import React, { useState, useEffect } from 'react';

export default function RecipeList(props) {
  return (
    <div>
      <h1 className="title">I am in the recipe section</h1>
      {props.name}
    </div>
  )
}
