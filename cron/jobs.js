const cron = require('node-cron');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const DailyData = require('../models/DailyData');

// Helper to get today's date in YYYY-MM-DD
const getTodayString = () => {
  const d = new Date();
  return d.toISOString().split('T')[0];
};

// Function to fetch data and save to MongoDB
const fetchAndSaveAstrologyData = async () => {
  try {
    console.log('Running daily astrology data sync...');
    const today = getTodayString();
    
    // Check if we already have today's data
    const existing = await DailyData.findOne({ date: today });
    if (existing) {
      console.log('Data for today already exists.');
      return;
    }

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      console.error("GEMINI_API_KEY is not defined in environment variables.");
      return;
    }
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: "gemini-3.1-flash-lite" });

    const prompt = `Provide the daily astrology data for today (${today}) for Ahmedabad, Gujarat in JSON format.
The JSON must have exactly two root keys: "rashifal" and "panchang".
"rashifal" should be an object with the 12 zodiac signs (in lowercase english: aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces) and their horoscope for today in Gujarati language.
"panchang" should be an object with: "tithi", "nakshatra", "paksha", "masa", "sunrise", "sunset", "rahukaal", "abhijit_muhurta".
Return ONLY valid JSON without any markdown formatting like \`\`\`json.`;

    console.log('Calling Gemini 3.1 Flash API...');
    const result = await model.generateContent(prompt);
    let text = result.response.text();
    
    // Remove markdown code blocks if present
    if (text.startsWith('\`\`\`json')) {
      text = text.replace(/^\`\`\`json\\s*/, '').replace(/\\s*\`\`\`$/, '');
    } else if (text.startsWith('\`\`\`')) {
      text = text.replace(/^\`\`\`\\s*/, '').replace(/\\s*\`\`\`$/, '');
    }
    
    const parsedData = JSON.parse(text);

    // 3. Save to MongoDB
    const newData = new DailyData({
      date: today,
      rashifal: parsedData.rashifal || {},
      panchang: parsedData.panchang || {}
    });
    
    await newData.save();
    console.log('Successfully saved astrology data for', today);

  } catch (error) {
    console.error('Error in daily sync:', error);
  }
};

// Schedule job to run at 12:02 AM every day
const initCronJobs = () => {
  cron.schedule('2 0 * * *', () => {
    fetchAndSaveAstrologyData();
  });
  console.log('Cron jobs initialized for Gemini 3.1 Flash.');
};

module.exports = { initCronJobs, fetchAndSaveAstrologyData };
