import React from "react"
import LineChart from './LineChart'
import axios from 'axios'
// import socketIOClient from 'socket.io-client'
import { socket } from '../App' 

// let socket
let tempSensor = [];
class GraphPanel extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            isFetching: false,
            sensor: []
        }
        
        this.fetchAllSensorData = this.fetchAllSensorData.bind(this)
        this.getNewSensorData = this.getNewSensorData.bind(this)
        this.updateSensorData = this.updateSensorData.bind(this)

        // socket = socketIOClient('http://localhost:5050/')
        socket.on('new_sensor_data', this.getNewSensorData)
    }

    fetchAllSensorData() {
        this.setState({isFetching: true})

        axios.get('http://localhost:5050/sensors')
            .then(res => {
                this.setState({sensor: res.data, isFetching: false})
                tempSensor = [...res.data] // Get a copy of the initial data from this.state.sensor
            })
            .catch(err => {
                console.log(err)
                this.setState({isFetching: false})
            })
    }

    getNewSensorData(doc) {
        tempSensor = [...tempSensor, doc];
        if (tempSensor.length > 40) {
            tempSensor.shift();
        }

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
        this.setState({
            sensor: tempSensor
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
                <h3 style={{'fontSize': 'calc(12px + 1.2vw)', 'textAlign': 'center'}}>Line Graph</h3>
                <LineChart sensorData={this.state.sensor} />
            </div>
        )
    }
}

export default GraphPanel