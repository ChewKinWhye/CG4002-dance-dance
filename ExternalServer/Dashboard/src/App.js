import React from 'react'
import './App.css'
import DanceInfoPanel from './components/DanceInfoPanel'
import GraphPanel from './components/GraphPanel'
import ConsolePanel from './components/ConsolePanel'
import NavBar from './components/NavBar'
import Spinner from './components/Loading'
import { Container, Row, Col } from 'reactstrap'
import socketIOClient from 'socket.io-client'

let socket

class App extends React.Component {
  constructor(props) {
    super(props)

    this.state = {}
    socket = socketIOClient('http://localhost:5050/')
  }

  render() {
    return (
      <div className='AppContainer'>
        <div style={{'width': '35%', 'height': '100%'}}>
          <DanceInfoPanel />
        </div>
        <div style={{'width': '65%', 'height': '100%'}}>
          <div style={{'width': '100%', 'height': '70%'}}>
            <GraphPanel />
          </div>
          <div style={{'width': '100%', 'height': '30%'}}>
            <ConsolePanel />
          </div>
        </div> 
      </div>
    )
  }
}

export { App, socket }
