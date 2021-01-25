import React, { useEffect, useState } from 'react'
import { useHistory } from "react-router-dom";
import DrinkCard from './DrinkCard';
import { DOMAIN } from '../conf';

export default function Selection() {

    let [drinks, setDrinks] = useState([])
    let [pending, setPending] = useState(false)
    const history = useHistory();
    let resourceUrl = DOMAIN + "/drinks/"

    useEffect(() => {
        setPending(true)
        fetch(resourceUrl).then((response) => {
           return response.json() 
        }).then((data) => {
            setPending(false);
            console.log("data from drinks api", data);
            setDrinks(data)
        }).catch((err) => {
        console.log("could not get drink selection! Aborting", err, err.response)
        setPending(false)
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
        <div className="container">
            <div className="box">            
            <h1 id="selectionHeading">Select</h1>
            <div className="columns is-multiline">
                {pending?  <progress class="progress is-large is-info" max="100">60%</progress>
 : null}
            {drinks.map((drink) => {
                return (
                    <DrinkCard 
                        key={drink.id}
                        drink={drink}
                        onClick={drink => {}}
                    />
                )
            }
            )}

            </div>
                        </div>
        </div>
    )
}
