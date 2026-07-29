module.exports = {
  apps : [{
    name: 'node-service',
    script: 'app.js',
    instances: 2,
    exec_mode: 'cluster',
    max_memory_restart: '150M',
    error_file: 'logs/error.log',
    out_file: 'logs/out.log'
  }]
};
