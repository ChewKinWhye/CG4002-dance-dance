const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const predictionSchema = new Schema({
    danceMove: {type: Number, required: true},
    dancePos: {type: [Number], required: true},
    syncDelay: {type: Number, required: true},
    date: {type: Date, required: true}
})

const Prediction = mongoose.connection
                .useDb('dashboard-db')
                .model('Prediction', predictionSchema, 'predictions');

module.exports = Prediction;