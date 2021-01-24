import React, { useEffect, useState } from 'react'
import { useHistory } from "react-router-dom";
import { DOMAIN } from '../conf';

export default function Selection() {

    let [drinks, setDrinks] = useState([])
    const history = useHistory();
    let resourceUrl = DOMAIN + "/drinks/"

    useEffect(() => {
        fetch(resourceUrl).then((response) => {
           return response.json() 
        }).then((data) => {
            console.log("data from drinks api", data);
            setDrinks(data)
        }).catch((err) => {
	    console.log("could not get drink selection! Aborting", err, err.response)
	    history.push("/")
	})
    }, [history, resourceUrl])

    const selectDrink = (drink) => {
        fetch(resourceUrl, {
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
