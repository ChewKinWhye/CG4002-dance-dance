const router = require('express').Router();
let Sensor = require('../models/sensor.model');

// HTTP GET: Get all documents in sensors collection
router.route('/').get((req, res) => {
    Sensor.find()
        .then(sensors => res.json(sensors.slice(-40)))
        .catch(err => res.status(400).json('Error: ' + err));
});

// HTTP POST: Add a new document in sensors collection
router.route('/add').post((req, res) => {
    const sensorX1 = Number(req.body.sensorX1);
    const sensorY1 = Number(req.body.sensorY1);
    const sensorZ1 = Number(req.body.sensorZ1);

    const sensorX2 = Number(req.body.sensorX2);
    const sensorY2 = Number(req.body.sensorY2);
    const sensorZ2 = Number(req.body.sensorZ2);

    const sensorX3 = Number(req.body.sensorX3);
    const sensorY3 = Number(req.body.sensorY3);
    const sensorZ3 = Number(req.body.sensorZ3);

    const date = Date.parse(req.body.date);

    const newSensor = new Sensor({
        sensorX1,
        sensorY1,
        sensorZ1,

        sensorX2,
        sensorY2,
        sensorZ2,

        sensorX3,
        sensorY3,
        sensorZ3,
        
        date
    });

    newSensor.save()
        .then(() => res.json('New sensor data added.'))
        .catch(err => res.status(400).json('Error: '+ err));
});

module.exports = router;