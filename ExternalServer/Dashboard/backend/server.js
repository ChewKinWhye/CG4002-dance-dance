const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');

require('dotenv').config();

const app = express();
const server = require('http').Server(app);
const io = require('socket.io')(server);

let Prediction = require('./models/prediction.model');

// Use port from environment if specified, otherwise use port 5000. 
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Setup mongoose.
const uri = process.env.ATLAS_URI;
mongoose.connect(uri, { useNewUrlParser: true, useCreateIndex: true });
const connection = mongoose.connection;

let cachedSensorsResumeToken;
let cachedPredictionsResumeToken;

// Setup socket.io
io.on('connection', (client) => {
    console.log('New client connected: ' + client.id)

    // client.on('init_sensor_data', () => {
    //     // connection.useDb('dashboard-db').collection('sensors').find()
    //     //     .then( (sensors) =>  io.sockets.emit('populate_sensors_data', sensors) )
    //     //     .catch( (err) => { throw err } )
    // })

    // client.on('init_prediction_data', () => {
    //     console.log('i got here')
    //     let data = Prediction.find()
    //     client.emit('populate_predictions_data', data)
    //     console.log('i end up here')
    //     // const predictions = Prediction.find().
    //     // client.emit('populate_predictions_data', {
    //     //     danceMove: 99,
    //     //     date: Date.parse('2020-03-07T01:37:10.247+00:00')
    //     // })
        
    //     // io.sockets.emit('populate_predictions_data', predictions)

    //     // io.sockets.emit('populate_predictions_data', predictions)
    //     // connection.useDb('dashboard-db').collection('predictions').find()
    //     //     .then( (predictions) =>  io.sockets.emit('populate_predictions_data', predictions) )
    //     //     .catch( (err) => { throw err } )
    // })

    client.on('disconnect', () => {
        console.log('Client disconnected')
    })
})

connection.once('open', () => {
    console.log("MongoDB database connection established successfully");

    // Create a $match aggregation pipeline to filter out irrelevant changes.
    pipeline = [{
        $match: {operationType: {$in: ['insert', 'delete']}}
    }]

    // Watch for changes in the collection for sensors and predictions.
    const sensorsChangeStream = connection.useDb('dashboard-db').collection('sensors').watch(pipeline);
    const predictionsChangeStream = connection.useDb('dashboard-db').collection('predictions').watch(pipeline);

    // Perform action when new data is inserted to the sensors collection.
    sensorsChangeStream.on('change', (change) => {
        // console.log('new sensor')
        // console.log(change)
        // cachedSensorsResumeToken = change["_id"];
        if (change.operationType === 'insert') {
            const newDoc = change.fullDocument
            io.emit('new_sensor_data', newDoc)
        } else {
            // console.log('sensor deleted')
            // io.emit('sensor_data_deleted')
        }
        
    })
    sensorsChangeStream.on('error', () => {
        if (cachedSensorsResumeToken) {
            // establishChangeStream(cachedResumeToken)
        }
    })

    // Perform action when new data is inserted to the predictions collection.
    predictionsChangeStream.on('change', (change) => {
        // console.log('new prediction')
        // console.log(change)
        // cachedPredictionsResumeToken = change["_id"];
        if (change.operationType === 'insert') {
            const newDoc = change.fullDocument
            io.emit('new_prediction_data', newDoc)
        } else {
            // console.log('prediction deleted')
            // io.emit('prediction_data_deleted')
        }
        
    })
    predictionsChangeStream.on('error', () => {
        if (cachedPredictionsResumeToken) {
            // establishChangeStream(cachedResumeToken)
        }
    })
});

// Setup routes.
const sensorsRouter = require('./routes/sensors');
const predictionsRouter = require('./routes/predictions');
app.use('/sensors', sensorsRouter);
app.use('/predictions', predictionsRouter);

// Start listening to port.
server.listen(port, () => {
    console.log(`Server is running on port: ${port}`);
});
