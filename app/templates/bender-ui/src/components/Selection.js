import React, { useEffect, useState } from 'react'
import { useHistory } from "react-router-dom";
import DrinkCard from './DrinkCard';
import { DOMAIN } from '../conf';
import Pending from './Pending';

const NUMBER_PER_PAGE = 2;

export default function Selection() {

    let [drinks, setDrinks] = useState([])
    let [pending, setPending] = useState(false)
    let [selectedDrink, setSelectedDrink] = useState(false)
    let [pageNum, setPageNum] = useState(1);

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


    useEffect(() => {
        const timeoutID = window.setTimeout(() => {
            history.push("/")
        }, 160000); // customize with value from server in the future
    
        return () => window.clearTimeout(timeoutID );
    }, []);

    const selectDrink = (drink) => {
        let body = JSON.stringify({ drink_id: drink.id });
        console.log("selected ", drink.id, "Passing", body)
        setPending(true)
        setSelectedDrink(true)
        fetch(resourceUrl, {
            method: "POST",
            headers: {
                Accept: "application/json",
                'Content-Type': "application/json",
            },
            body: body,
        }).then(function (response) {
            setPending(false);
            return response.json();
        }).then(function (data) {
            setPending(false);
            history.push("/enjoy");
        }).catch((err) => {
           setPending(false);
            console.log('error starting drink', err, err.response);
        });
    }

    const getPending = () => {
        let message = "Loading Selection";
        console.log("displaying pending")
        if (selectedDrink) {
            message = "Preparing your drink..."
        }
        return <Pending message={message}/>
    }
    
    const paginate = () => {
        return drinks.slice((pageNum - 1) * NUMBER_PER_PAGE, NUMBER_PER_PAGE * pageNum);
    }
    
    const goBack = () => {
        let min = 0;
        if (pageNum - 1 > min) {
             setPageNum(pageNum - 1)
        }
    }
    
    const goForward = () => {
        let max = Math.ceil(drinks.length / NUMBER_PER_PAGE)
        if (pageNum + 1 <= max) {
             setPageNum(pageNum + 1)
        }
    }

    return (
        <div className="container">
            <div className="box" style={{
                margin: 0
            }}>
                {pending ? getPending() : (
                    <div>
                <div className="columns is-multiline">
                    {paginate(drinks).map((drink) => {
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
                    <div className="columns">
                        <div className="column is-5"></div>
                        <div className="column">
                            <div className="columns is-justify-content-space-between">
                                <div className="button is-dark p-4" onClick={goBack}>{"<"}</div>
                                <div className="button is-dark p-4" onClick={goForward}>{">"}</div>    
                            </div>                        
                        </div>
                        <div className="column is-5"></div>
                    </div>
                </div>
                )}
            </div>
        </div>
    )
}
