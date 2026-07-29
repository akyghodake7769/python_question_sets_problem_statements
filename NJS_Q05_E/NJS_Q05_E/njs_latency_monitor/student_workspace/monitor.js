const { monitorEventLoopDelay } = require('perf_hooks');

const h = monitorEventLoopDelay({ resolution: 10 });
h.enable();

function getStats() {
    return {
        min: h.min / 1e6,
        max: h.max / 1e6,
        mean: h.mean / 1e6,
        p95: h.percentile(95) / 1e6
    };
}

module.exports = { getStats };
