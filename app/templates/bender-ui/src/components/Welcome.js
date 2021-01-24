import React from 'react'
import { useHistory } from 'react-router-dom'

export default function Welcome() {

    const history = useHistory()

    const wake = () => {
      fetch("localhost:8000", {
          method: "POST",
      }).then((response) => {
        history.push("selection")
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
