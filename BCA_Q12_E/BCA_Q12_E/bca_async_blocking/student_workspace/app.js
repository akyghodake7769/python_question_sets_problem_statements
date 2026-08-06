const fs = require('fs').promises;
async function handleRequest(req, res) {
  const data = await fs.readFile('data.json', 'utf-8');
  return data;
}
module.exports = { handleRequest };
