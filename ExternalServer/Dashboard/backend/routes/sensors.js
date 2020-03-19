const router = require('express').Router();
let Sensor = require('../models/sensor.model');

router.route('/dancer1').get((req, res) => {
    Sensor.find({ dancerId: 1 })
        .then(dancer1 => res.json(dancer1.slice(-40)))
        .catch(err => res.status(400).json('Error: ' + err));
});

router.route('/dancer2').get((req, res) => {
    Sensor.find({ dancerId: 2 })
        .then(dancer2 => res.json(dancer2.slice(-40)))
        .catch(err => res.status(400).json('Error: ' + err));
});

router.route('/dancer3').get((req, res) => {
    Sensor.find({ dancerId: 3 })
        .then(dancer3 => res.json(dancer3.slice(-40)))
        .catch(err => res.status(400).json('Error: ' + err));
});

// HTTP POST: Add a new document in sensors collection
router.route('/add').post((req, res) => {
    const dancerId = Number(req.body.dancerId);
    const sensorAX = Number(req.body.sensorAX);
    const sensorAY = Number(req.body.sensorAY);
    const sensorAZ = Number(req.body.sensorAZ);
    // const sensorGX = Number(req.body.sensorGX);
    // const sensorGY = Number(req.body.sensorGY);
    // const sensorGZ = Number(req.body.sensorGZ);
    const date = Date.parse(req.body.date);

    const newSensor = new Sensor({
        dancerId,

        sensorAX,
        sensorAY,
        sensorAZ,

        // sensorGX,
        // sensorGY,
        // sensorGZ,
        
        date
    });

    newSensor.save()
        .then(() => res.json('New sensor data added.'))
        .catch(err => res.status(400).json('Error: '+ err));
});

module.exports = router;