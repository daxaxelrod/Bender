import React, { useState } from 'react'
import { useHistory } from 'react-router-dom';
import { DOMAIN } from '../conf';
import Pending from './Pending';

export default function Welcome() {

    const history = useHistory()
    const [pending, setPending] = useState(false)

    const wake = () => {
        setPending(true)
        fetch(DOMAIN + "/wake/", {
            method: "POST",
        }).then((response) => {
            return response.json();
        })
        .then((response) => {
            setPending(false)
            history.push("drinks")
        }).catch((err) => {
            console.log("issue waking machine", err, err.response)
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
                        {pending ? <Pending message="Loading..."/> : (
                            <div className="buttons is-centered">
                                <button className="button is-primary is-size-3" onClick={wake}>Start</button>
                            </div>
                        )}
                    </div>
                </div>
                <div className="column"></div>
            </div>
        </div>
    )
}
