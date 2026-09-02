const { fetchAndSaveAstrologyData } = require('./cron/jobs');

(async () => {
  await fetchAndSaveAstrologyData();
})();
