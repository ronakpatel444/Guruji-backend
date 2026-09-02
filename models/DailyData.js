const mongoose = require('mongoose');

const dailyDataSchema = new mongoose.Schema({
  date: { type: String, required: true, unique: true }, // Format: YYYY-MM-DD
  rashifal: { type: Object, required: true }, // Gemini API result for 12 signs
  panchang: { type: Object, required: true }, // Panchang API result
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('DailyData', dailyDataSchema);
