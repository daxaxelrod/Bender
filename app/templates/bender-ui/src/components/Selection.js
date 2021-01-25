import React, { useEffect, useState } from 'react'
import { useHistory } from "react-router-dom";
import DrinkCard from './DrinkCard';
import { DOMAIN } from '../conf';
import Pending from './Pending'

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
        let body = JSON.stringify({ drink_id: drink.id });
        console.log("selected ", drink.id, "Passing", body)
        fetch(resourceUrl, {
            method: "POST",
            headers: {
                Accept: "application/json",
                'Content-Type': "application/json",
            },
            body: body,
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
            history.push("/enjoy");
        }).catch((err) => {
            console.log('error starting drink', err, err.response);
        });
    }

    const getPending = () => {
        return <Pending />
    }

    return (
        <div className="container">
            <div className="box">
                <h1 className="pageHeading">Select</h1>
                {pending ? getPending() : null}
                <div className="columns is-multiline">
                    {drinks.map((drink) => {
                        return (
                            <DrinkCard
                                key={drink.id}
                                drink={drink}
                                onClick={() => selectDrink(drink)}
                            />
                        )
                    }
                    )}

                </div>
            </div>
        </div>
    )
}
