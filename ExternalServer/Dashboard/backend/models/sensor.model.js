const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const sensorSchema = new Schema({
    dancerId: {type: Number, required: true},
    sensorAX: {type: Number, required: true},
    sensorAY: {type: Number, required: true},
    sensorAZ: {type: Number, required: true},
    // sensorGX: {type: Number, required: true},
    // sensorGY: {type: Number, required: true},
    // sensorGZ: {type: Number, required: true},

    // sensorX2: {type: Number, required: true},
    // sensorY2: {type: Number, required: true},
    // sensorZ2: {type: Number, required: true},

    // sensorX3: {type: Number, required: true},
    // sensorY3: {type: Number, required: true},
    // sensorZ3: {type: Number, required: true},

    date: {type: Date, required: true}
})

const Sensor = mongoose.connection
                .useDb('dashboard-db')
                .model('Sensor', sensorSchema, 'sensors');

module.exports = Sensor;