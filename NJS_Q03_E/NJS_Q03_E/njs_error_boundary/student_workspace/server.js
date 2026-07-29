const express = require('express');
const app = express();

process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err.message);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
    process.exit(1);
});

app.get('/error', (req, res, next) => {
    // Simulate async error
    Promise.reject(new Error("Async Database Failure")).catch(next);
});

app.use((err, req, res, next) => {
    res.status(500).json({ error: err.message });
});

module.exports = app;
