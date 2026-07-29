// server.js using worker.js for offloading pbkdf2 workload
const express = require('express');
const { Worker } = require('worker_threads');
const path = require('path');
const app = express();

app.get('/hash', (req, res) => {
    const password = req.query.password || 'secret';
    const worker = new Worker(path.join(__dirname, 'worker.js'), {
        workerData: password
    });
    worker.on('message', (hash) => {
        res.json({ hash });
    });
    worker.on('error', (err) => {
        res.status(500).json({ error: err.message });
    });
});

module.exports = app;
