import React from "react"
import HistoryList from "./HistoryPanel"
import axios from 'axios'
import '../App.css'
import { socket } from '../App' 

// let socket
class DanceInfoPanel extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            isFetching: false,
            firstReceived: true,
            dance: []
        }
        
        this.fetchAllDanceData = this.fetchAllDanceData.bind(this)
        this.getNewDanceData = this.getNewDanceData.bind(this)

        // socket = socketIOClient('http://localhost:5050/')
        socket.on('new_prediction_data', this.getNewDanceData)
    }

    fetchAllDanceData(docs) {
        this.setState({isFetching: true})

        // this.setState({
        //     dance: docs,
        //     isFetching: false
        // })

        axios.get('http://localhost:5050/predictions')
            .then(res => {
                this.setState({dance: res.data, isFetching: false})
            })
            .catch(err => {
                console.log(err)
                this.setState({isFetching: false})
            })
    }

    getNewDanceData(doc) {
        this.setState({isFetching: true})

        this.setState(prevState => ({
            dance: [doc, ...prevState.dance]
        }))

        if (this.state.dance.length > 10) {
            let newArr = [...this.state.dance]
            newArr.pop()

            this.setState({
                dance: newArr
            })
        }

        if (this.state.firstReceived) {
            this.setState({firstReceived: false})
        }

        this.setState({isFetching: false})
    }

    displayDanceMove() {
        let dance = [...this.state.dance]
        
        if (dance.length) {
            console.log('it contains data')
            return dance[0].danceMove
        } else {
            console.log('i got here')
            return 'Waiting...'
        }
    }

    componentDidMount() {
        this.fetchAllDanceData()
        // socket.emit('init_prediction_data')
        // socket.on('populate_predictions_data', this.fetchAllDanceData)
        

        // this.timer = setInterval(() => this.updateDanceData(), 500)
    }

    // componentWillUnmount() {
    //     clearInterval(this.timer)
    //     this.timer = null
    // }

    render() {
        let dance = [...this.state.dance]

        return (
            <div className='Container'>
                <div style={{
                    'width': '100%',
                    'height': '30%',
                    'textAlign': 'center',
                    'backgroundColor': '#0084ff',
                    'color': 'white',
                    'borderBottomLeftRadius': '12px',
                    'borderBottomRightRadius': '12px'
                    }}
                >
                    <h1 style={{'fontSize': 'calc(12px + 1.2vw)'}}>Current Dance Move</h1>
                    <h2 style={{'fontSize': 'calc(10px + 1.0vw)'}}>Dance Number: {
                        (dance.length && !this.state.firstReceived)? dance[0].danceMove.toString() : 'Waiting...'
                    }</h2>
                    <h3 style={{'fontSize': 'calc(8px + 0.9vw)'}}>Dancer Position: {
                        (dance.length && !this.state.firstReceived)? dance[0].dancePos.toString() : 'Waiting...'
                    }</h3>
                    <h3 style={{'fontSize': 'calc(8px + 0.9vw)'}}>Sync Delay: {
                        (dance.length && !this.state.firstReceived)? dance[0].syncDelay.toFixed(2) + ' seconds' : 'Waiting...'
                    }</h3>
                    <br />
                </div>
                <div style={{
                    'width': '100%', 
                    'height': '5%', 
                    'textAlign': 'center',
                    'backgroundColor': '#41688d',
                    'color': 'white',
                    'borderTopLeftRadius': '12px',
                    'borderTopRightRadius': '12px'
                    }}
                >
                    <h2 style={{'fontSize': 'calc(10px + 1.0vw'}}>History (10 most recent)</h2>
                </div>
                <div style={{'width': '100%', 'height': '65%', 'backgroundColor': '#4072a0'}}>
                    <HistoryList danceData={this.state.dance} firstReceived={this.state.firstReceived} />
                </div>
            </div>
        )
    }
} 

export default DanceInfoPanel