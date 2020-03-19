import React from "react"
import { Button, Form, FormGroup, Label, Input, FormText } from 'reactstrap';

function ConsolePanel() {
    return (
        <div className='Container'>
            <div style={{'width': '100%', 'height': '80%'}}>
                <Input style={{'height': '100%', 'backgroundColor': '#0d252edc', 'resize': 'none'}} type='textarea' readOnly />
            </div>
            <div style={{'width': '100%', 'height': '20%'}}>
                <Input style={{'height': '100%'}} type='text' placeholder='Enter command...' />
            </div>
            {/* <FormGroup style={{'height': '100%', 'backgroundColor': 'pink'}}> */}
                {/* <Input type="textarea" readOnly/> */}
            {/* </FormGroup> */}
            {/* <FormGroup style={{'height': '30%', 'backgroundColor': 'purple'}}> */}
                {/* <Input type="text" placeholder="Enter command.." /> */}
            {/* </FormGroup> */}
        </div>
    )
}

export default ConsolePanel