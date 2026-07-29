const express = require('express');
const app = express();

// LEAK: Cache grows infinitely. Patch it to keep maximum 100 elements.
const cache = new Map();

app.get('/api/track', (req, res) => {
    const id = req.query.id || 'default';
    cache.set(id, { timestamp: Date.now(), metadata: req.headers });
    
    if (cache.size > 100) {
        const firstKey = cache.keys().next().value;
        cache.delete(firstKey);
    }
    
    res.json({ tracked: true, cacheSize: cache.size });
});

module.exports = app;
