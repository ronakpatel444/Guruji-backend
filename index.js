require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const { initCronJobs, fetchAndSaveAstrologyData } = require('./cron/jobs');
const DailyData = require('./models/DailyData');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/astromaster';

// Connect to MongoDB
mongoose.connect(MONGO_URI)
  .then(() => {
    console.log('Connected to MongoDB');
    // Start Cron jobs
    initCronJobs();
    
    // Optional: Fetch immediately on startup if missing
    fetchAndSaveAstrologyData();
  })
  .catch(err => console.error('MongoDB connection error:', err));

// API Endpoint for Flutter App to get Today's Data
app.get('/api/daily-astrology', async (req, res) => {
  try {
    const d = new Date();
    const today = d.toISOString().split('T')[0];
    
    let data = await DailyData.findOne({ date: today });
    
    if (!data) {
      return res.status(404).json({ error: 'Data for today is not available yet.' });
    }
    
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
