const fs = require('fs');

const config = {
    port: process.env.PORT || 3000,
    env: process.env.NODE_ENV || 'development',
    dbUrl: process.env.DB_URL || 'mongodb://localhost:27017/test'
};

fs.writeFileSync('config_report.json', JSON.stringify(config, null, 2));
console.log("Config report generated successfully.");
