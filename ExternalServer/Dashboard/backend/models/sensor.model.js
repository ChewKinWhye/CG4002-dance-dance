const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const sensorSchema = new Schema({
    sensorX1: {type: Number, required: true},
    sensorY1: {type: Number, required: true},
    sensorZ1: {type: Number, required: true},

    sensorX2: {type: Number, required: true},
    sensorY2: {type: Number, required: true},
    sensorZ2: {type: Number, required: true},

    sensorX3: {type: Number, required: true},
    sensorY3: {type: Number, required: true},
    sensorZ3: {type: Number, required: true},

    date: {type: Date, required: true}
})

const Sensor = mongoose.connection
                .useDb('dashboard-db')
                .model('Sensor', sensorSchema, 'sensors');

module.exports = Sensor;