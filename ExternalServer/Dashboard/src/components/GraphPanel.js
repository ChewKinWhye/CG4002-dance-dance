import React from "react"
import LineChart from './LineChart'
import axios from 'axios'
// import socketIOClient from 'socket.io-client'
import { socket } from '../App' 

// let socket
let tempSensor = [];

let tempDancer1 = [];
let tempDancer2 = [];
let tempDancer3 = [];

class GraphPanel extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            isFetching: false,
            sensor: [],
            dancer1: [],
            dancer2: [],
            dancer3: []
        }
        
        this.fetchAllSensorData = this.fetchAllSensorData.bind(this)
        this.getNewSensorData = this.getNewSensorData.bind(this)
        this.updateSensorData = this.updateSensorData.bind(this)

        // socket = socketIOClient('http://localhost:5050/')
        socket.on('new_sensor_data', this.getNewSensorData)
    }

    fetchAllSensorData() {
        this.setState({isFetching: true})
        axios.get('http://localhost:5050/sensors/dancer1')
            .then(res => {
                this.setState({dancer1: res.data, isFetching: false})
                tempDancer1 = [...res.data] // Get a copy of the initial data from this.state.dancer1
            })
            .catch(err => {
                console.log(err)
                this.setState({isFetching: false})
            })

        this.setState({isFetching: true})
        axios.get('http://localhost:5050/sensors/dancer2')
            .then(res => {
                this.setState({dancer2: res.data, isFetching: false})
                tempDancer2 = [...res.data] // Get a copy of the initial data from this.state.dancer1
            })
            .catch(err => {
                console.log(err)
                this.setState({isFetching: false})
            })

        this.setState({isFetching: true})
        axios.get('http://localhost:5050/sensors/dancer3')
            .then(res => {
                this.setState({dancer3: res.data, isFetching: false})
                tempDancer3 = [...res.data] // Get a copy of the initial data from this.state.dancer1
            })
            .catch(err => {
                console.log(err)
                this.setState({isFetching: false})
            })
    }

    getNewSensorData(doc) {
        // Check from which dancer the sensor data is coming from.
        if (doc.dancerId == 1) {
            tempDancer1 = [...tempDancer1, doc]
            if (tempDancer1.length > 40) {
                tempDancer1.shift()
            }
        } else if (doc.dancerId == 2) {
            tempDancer2 = [...tempDancer2, doc]
            if (tempDancer2.length > 40) {
                tempDancer2.shift()
            }
        } else if (doc.dancerId == 3) {
            tempDancer3 = [...tempDancer3, doc]
            if (tempDancer3.length > 40) {
                tempDancer3.shift()
            }
        }

        // tempSensor = [...tempSensor, doc];
        // if (tempSensor.length > 40) {
        //     tempSensor.shift();
        // }

        // this.setState({isFetching: true})

        // this.setState(prevState => ({
        //     sensor: [...prevState.sensor, doc]
        // }))

        // if (this.state.sensor.length > 40) {
        //     let newArr = [...this.state.sensor]
        //     newArr.shift()

        //     this.setState({
        //         sensor: newArr
        //     })
        // }

        // this.setState({isFetching: false})
    }

    updateSensorData() {
        // this.setState({
        //     sensor: tempSensor
        // })
        this.setState({
            dancer1: tempDancer1,
            dancer2: tempDancer2,
            dancer3: tempDancer3
        })  
    }

    componentDidMount() {
        this.fetchAllSensorData()
        
        this.timer = setInterval(() => this.updateSensorData(), 100)
    }

    componentWillUnmount() {
        clearInterval(this.timer)
        this.timer = null
    }

    render() {
        return (
            <div className='Container'>
                <h3 style={{'height': '10%', 'fontSize': 'calc(12px + 1.2vw)', 'textAlign': 'center'}}>Line Graph</h3>
                <div style={{'height': '90%'}}>
                    <LineChart dancerId={1} sensorData={this.state.dancer1} />
                    <LineChart dancerId={2} sensorData={this.state.dancer2} />
                    <LineChart dancerId={3} sensorData={this.state.dancer3} />
                </div>
                
            </div>
        )
    }
}

export default GraphPanel