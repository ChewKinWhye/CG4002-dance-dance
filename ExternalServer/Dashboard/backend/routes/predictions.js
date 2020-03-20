const router = require('express').Router();
let Prediction = require('../models/prediction.model');

// HTTP GET: Get all documents in predictions collection
router.route('/').get((req, res) => {
    Prediction.find().sort({ date: -1 }).limit(10)
        .then(predictions => res.json(predictions))
        .catch(err => res.status(400).json('Error: ' + err));
});

// HTTP POST: Add a new document in predictions collection
router.route('/add').post((req, res) => {
    const danceMove = Number(req.body.danceMove);
    const dancePos = req.body.dancePos;
    const syncDelay = Number(req.body.syncDelay);
    const date = Date.parse(req.body.date);

    const newPrediction = new Prediction({
        danceMove,
        dancePos,
        syncDelay,
        date
    });

    newPrediction.save()
        .then(() => res.json('New prediction added.'))
        .catch(err => res.status(400).json('Error: '+ err));
});

module.exports = router;