const express = require('express');
const app = express();
app.use(express.json());
app.post('/api/users', (req, res) => {
  if (!req.body.username) {
    return res.status(400).json({ error: 'Username required' });
  }
  return res.status(201).json({ id: 1, username: req.body.username });
});
