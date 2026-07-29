const { parentPort, workerData } = require('worker_threads');
const crypto = require('crypto');

const password = workerData;
// CPU intensive work
const hash = crypto.pbkdf2Sync(password, 'salt', 100000, 64, 'sha512').toString('hex');
parentPort.postMessage(hash);
