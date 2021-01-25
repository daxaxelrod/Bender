import React from 'react'

export default function DrinkCard({ onClick, drink }) {

    let missingIngredients = drink.instructions.filter(((instruction) => {
        return instruction.ingredient.resevoir == null
    }))
    let isAvailable = missingIngredients.length == 0;
    const allowClick = isAvailable ? onClick : () => { }

    const getAverageCost = () => {
        //naive rn
        return Math.round(drink.instructions.reduce((acc, instruction) => {
            return acc + instruction.ingredient.cost.length
        }, 0) / drink.instructions.length)
    }

    const getPartsList = () => {
        // 3 parts x, 1 part y

        let totalPour = drink.instructions.reduce((sum, i) => sum + i.pour_duration, 0)
        let lowest_percentage = 100;
        for (let i = 0; i < drink.instructions.length; i++) {
            const part = drink.instructions[i].pour_duration / totalPour;
            if (part < lowest_percentage) {
                lowest_percentage = part
            }
        }

        return drink.instructions.map((instruction, idx) => {
            // i crack myself up
            let pourPortion = instruction.pour_duration / totalPour
            let part = Math.round(pourPortion / lowest_percentage)
            let result = `${part} part${part > 1 ? 's' : ''} ${instruction.ingredient.name}`
            let comma = drink.instructions.length - 1 === idx ? "" : ", "
            return <p key={`instruction-${instruction.id}`} className="drink-option__description">{result + comma}</p>
        })

    }

    const getUnavailableOverlay = () => {
        return (
            <div className="drink-unavailable">
                <p className="drink-unavailable__text">Unavailable</p>
            </div>
        )
    }

    return (
        <div className="column is-half">
            <div className={"box drink-option"} onClick={allowClick}>
                {isAvailable ? null : getUnavailableOverlay()}
                <div className="drink-option__name">{drink.name}</div>
                <div className="columns">
                    <div className="column">
                        {getPartsList()}
                    </div>
                    <div className="column drink-price">
                        <p className="drink-option__description" >{"$".repeat(getAverageCost())}</p>
                    </div>
                </div>
            </div>
        </div>
    )
}
