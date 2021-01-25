import React from 'react'
import { Windmill } from 'react-activity';

export default function Pending({message}) {
    return (
        <div className="pending__container is-centered">
            <div className="pending_spinner is-centered">
                <Windmill color="#727981" size={34} speed={1} animating={true} />
            </div>
            <p className="pending__subtext">{message}</p>
        </div>
    )
}

Pending.defaultProps = {
    message: "Pending..."
}