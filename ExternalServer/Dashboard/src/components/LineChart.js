import React, { PureComponent } from 'react';
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';
import { mockComponent } from 'react-dom/test-utils';

const data = [
  {
    name: 'Page A', uv: 4000, pv: 2400, amt: 2400,
  },
  {
    name: 'Page B', uv: 3000, pv: 1398, amt: 2210,
  },
  {
    name: 'Page C', uv: 2000, pv: 9800, amt: 2290,
  },
  {
    name: 'Page D', uv: 2780, pv: 3908, amt: 2000,
  },
  {
    name: 'Page E', uv: 1890, pv: 4800, amt: 2181,
  },
  {
    name: 'Page F', uv: 2390, pv: 3800, amt: 2500,
  },
  {
    name: 'Page G', uv: 3490, pv: 4300, amt: 2100,
  },
];

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

  render() {
    // const sensors = this.props.sensorData.slice(Math.max(this.props.sensorData.length - 10, 0))
    const sensors = this.props.sensorData

    return (
      <div className='Container'>
        <ResponsiveContainer height='30%'>
          <LineChart
            data={sensors}
            margin={{
              top: 0, right: 35, left: 0, bottom: 0,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke='#183e62' />
            <XAxis dataKey="date" tick={{ fontSize: '12px'}} tickFormatter={this.dateFormat} />
            <YAxis />
            <Tooltip />
            {/* <Legend /> */}
            <Line type="monotone" dataKey="sensorX1" stroke="#ca8282" dot={false} />
            <Line type="monotone" dataKey="sensorY1" stroke="#a2ca82" />
            <Line type="monotone" dataKey="sensorZ1" stroke="#82b9ca" />
          </LineChart>
        </ResponsiveContainer>

        <ResponsiveContainer height='30%'>
          <LineChart
            data={sensors}
            margin={{
              top: 0, right: 35, left: 0, bottom: 0,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke='#183e62' />
            <XAxis dataKey="date" tick={{ fontSize: '12px'}} tickFormatter={this.dateFormat} />
            <YAxis />
            <Tooltip PopperProps={{ style: { pointerEvents: 'none' } }} />
            {/* <Legend /> */}
            <Line type="monotone" dataKey="sensorX2" stroke="#ca8282" />
            <Line type="monotone" dataKey="sensorY2" stroke="#a2ca82" />
            <Line type="monotone" dataKey="sensorZ2" stroke="#82b9ca" />
          </LineChart>
        </ResponsiveContainer>

        <ResponsiveContainer height='30%'>
          <LineChart
            data={sensors}
            margin={{
              top: 0, right: 35, left: 0, bottom: 0,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke='#183e62' />
            <XAxis dataKey="date" tick={{ fontSize: '12px'}} tickFormatter={this.dateFormat} />
            <YAxis />
            <Tooltip PopperProps={{ style: { pointerEvents: 'none' } }} />
            {/* <Legend /> */}
            <Line type="monotone" dataKey="sensorX3" stroke="#ca8282" />
            <Line type="monotone" dataKey="sensorY3" stroke="#a2ca82" />
            <Line type="monotone" dataKey="sensorZ3" stroke="#82b9ca" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }
}
