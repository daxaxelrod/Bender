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
        <div>
            <h1>Bender</h1>
            <div className="btn" onClick={wake}>
                <h2>Start</h2>
            </div>
        </div>
    )
}
