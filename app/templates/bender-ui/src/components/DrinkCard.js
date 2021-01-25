import React from 'react'

export default function DrinkCard({onClick, drink}) {

    let missingIngredients = drink.instructions.filter(((instruction) => {
      return instruction.ingredient.resevoir == null
    }))
    let isAvailable = missingIngredients.length == 0;
    const allowClick = isAvailable ? onClick : () => {}

    return (
        <div className="box" onClick={allowClick}>
            <div>{drink.name}</div>
            <p>{drink.cost}</p>
        </div>
    )
}
