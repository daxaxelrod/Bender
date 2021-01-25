import React from 'react'
import { useHistory } from 'react-router-dom';
import { DOMAIN } from '../conf';

import drink_1 from '../stock_drink_1.jpeg'

export default function Welcome() {

    const history = useHistory()

    const wake = () => {
        fetch(DOMAIN + "/wake/", {
            method: "POST",
        }).then((response) => {
            history.push("drinks")
        }).catch((err) => {
            console.log("issue waking machine")
        })
    }


    return (

        <div className="hero is-fullheight has-background-dark has-background">
            <img alt="Fill Murray" className="hero-background is-transparent" src={drink_1} />
            <div className="hero-body">
                <div className="container">
                    <div className="columns">
                        <div className="column">
                            <div className="box">
                                <h2 style={{ textAlign: "center", 
                                                                    paddingBottom: "1rem",
                                                                    fontSize: "7rem",
                                                                    fontFamily: "Pinyon Script" }}>Bender</h2>
                                <div className="buttons is-centered">
                                    <button className="button is-primary is-size-3" onClick={wake}>Start</button>
                                </div>
                            </div>
                        </div>
                        <div className="column"></div>
                    </div>

                </div>
            </div>
        </div>

    )
}
