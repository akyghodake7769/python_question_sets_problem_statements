const v8 = require('v8');
const fs = require('fs');

function checkMemory() {
    const mem = process.memoryUsage();
    // RSS memory threshold: 200MB = 200 * 1024 * 1024
    if (mem.rss > 200 * 1024 * 1024) {
        if (!fs.existsSync('Shared/diagnostics')) {
            fs.mkdirSync('Shared/diagnostics', { recursive: true });
        }
        const file = `Shared/diagnostics/heap-${Date.now()}.heapsnapshot`;
        v8.writeHeapSnapshot(file);
        console.log('Heap snapshot captured:', file);
    }
}

module.exports = { checkMemory };
