import React from 'react'
import { Link } from 'react-router-dom'

export default function Enjoy() {
    return (
        <div className="container">
            <div className="box">
                <h1 className="pageHeading mb-4">Enjoy!</h1>
                <Link to="/">
                    <div className="buttons is-centered">
                        <button className="button is-primary is-size-4">Start Over</button>
                    </div>
                </Link>
            </div>
        </div>
        
    )
}
