import React, { PureComponent } from 'react';
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';
import { mockComponent } from 'react-dom/test-utils';

// const data = [
//   {
//     name: 'Page A', uv: 4000, pv: 2400, amt: 2400,
//   },
//   {
//     name: 'Page B', uv: 3000, pv: 1398, amt: 2210,
//   },
//   {
//     name: 'Page C', uv: 2000, pv: 9800, amt: 2290,
//   },
//   {
//     name: 'Page D', uv: 2780, pv: 3908, amt: 2000,
//   },
//   {
//     name: 'Page E', uv: 1890, pv: 4800, amt: 2181,
//   },
//   {
//     name: 'Page F', uv: 2390, pv: 3800, amt: 2500,
//   },
//   {
//     name: 'Page G', uv: 3490, pv: 4300, amt: 2100,
//   },
// ];

export default class Example extends PureComponent {
  
  dateFormat(tickItem) {
    const d = new Date(tickItem)

    const hours = d.getHours()
    const minutes = d.getMinutes()
    const seconds = d.getSeconds()

    return ((hours < 10? '0' + hours : hours) 
      + ':' 
      + (minutes < 10? '0' + minutes : minutes) 
      + ':' 
      + (seconds < 10? '0' + seconds : seconds))
  }

  tooltipFormat(value, name, props) {
    switch (props.dancerId) {
      case 1:
        if (name.includes('X')) {
          return [value, 'sensor1_AX']
        } else if (name.includes('Y')) {
          return [value, 'sensor1_AY']
        } else if (name.includes('Z')) {
          return [value, 'sensor1_AZ']
        }
        break;
      case 2:
        if (name.includes('X')) {
          return [value, 'sensor2_AX']
        } else if (name.includes('Y')) {
          return [value, 'sensor2_AY']
        } else if (name.includes('Z')) {
          return [value, 'sensor2_AZ']
        }
        break;
      case 3:
        if (name.includes('X')) {
          return [value, 'sensor3_AX']
        } else if (name.includes('Y')) {
          return [value, 'sensor3_AY']
        } else if (name.includes('Z')) {
          return [value, 'sensor3_AZ']
        }
        break;
      default:
        return ['value', 'name']
    }
  }

  render() {
    // const sensors = this.props.sensorData.slice(Math.max(this.props.sensorData.length - 10, 0))
    const sensors = this.props.sensorData
    const dancerId = this.props.dancerId

    return (
      <div style={{'height': '33%'}}>
        <ResponsiveContainer height='100%'>
          <LineChart
            data={sensors}
            margin={{
              top: 0, right: 35, left: 0, bottom: 0,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke='#183e62' />
            <XAxis dataKey="date" tick={{ fontSize: '12px'}} tickFormatter={this.dateFormat} />
            <YAxis />
            <Tooltip formatter={(value, name, props) => { return [value, name + '_' + dancerId]}} />
            {/* <Legend /> */}
            <Line type="monotone" dataKey="sensorAX" stroke="#ca8282" />
            <Line type="monotone" dataKey="sensorAY" stroke="#a2ca82" />
            <Line type="monotone" dataKey="sensorAZ" stroke="#82b9ca" />
            {/* <Line type="monotone" dataKey="sensorGX" stroke="#4d9240" />
            <Line type="monotone" dataKey="sensorGY" stroke="#525a0b" />
            <Line type="monotone" dataKey="sensorGZ" stroke="#e712a7" /> */}
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }
}
