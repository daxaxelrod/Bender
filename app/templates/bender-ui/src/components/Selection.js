import React, { useEffect, useState } from 'react'
import { useHistory } from "react-router-dom";

export default function Selection() {

    let [drinks, setDrinks] = useState([])
    const history = useHistory();

    useEffect(() => {
        fetch("localhost:8000/selection").then((response) => {
            setDrinks(response.json())
        })
    }, [])

    const selectDrink = (drink) => {
        fetch('https://api.github.com/gists', {
            method: 'post',
            body: JSON.stringify({
                drink_id: drink.id
            })
          }).then(function(response) {
            // drink finished
            history.push("/enjoy");
            return response.json();
          }).then(function(data) {
            console.log('error starting drink');
          });
        
    }
    return (
        <div>
            <h1>Make a selection</h1>
            {drinks.map((drink) => {
                return (
                    <div onClick={selectDrink}>
                        <h3>{drink.name}</h3>
                        <p>{drink.cost}</p>
                    </div>
                )
            }
            )}
        </div>
    )
}
