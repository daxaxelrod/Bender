import React from 'react'
import { useHistory } from 'react-router-dom';
import { DOMAIN } from '../conf';

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
        <div className="container">
            <div className="columns">
                <div className="column">
                    <div className="box">
                        <h2 style={{
                            textAlign: "center",
                            paddingBottom: "1rem",
                            fontSize: "7rem",
                            fontFamily: "Pinyon Script"
                        }}>Bender</h2>
                        <div className="buttons is-centered">
                            <button className="button is-primary is-size-3" onClick={wake}>Start</button>
                        </div>
                    </div>
                </div>
                <div className="column"></div>
            </div>
        </div>
    )
}
