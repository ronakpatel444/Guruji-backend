const { getPanchangam, Observer, tithiNames, nakshatraNames } = require('@ishubhamx/panchangam-js');

// Coordinates for Ahmedabad, Gujarat
const observer = new Observer(23.0225, 72.5714, 50);

// Use current date and IST (+5:30)
const date = new Date();
const panchang = getPanchangam(date, observer, { timezoneOffset: 330 });

console.log("Location: Ahmedabad, Gujarat");
console.log("Date & Time: " + date.toString());
console.log("-----------------------------------------");
console.log("Tithi: " + tithiNames[panchang.tithi]);
console.log("Nakshatra: " + nakshatraNames[panchang.nakshatra]);
console.log("Paksha: " + panchang.paksha);
console.log("Masa: " + panchang.masa.name);
console.log("Sunrise: " + (panchang.sunrise ? panchang.sunrise.toLocaleTimeString() : 'N/A'));
console.log("Sunset: " + (panchang.sunset ? panchang.sunset.toLocaleTimeString() : 'N/A'));
console.log("-----------------------------------------");
console.log("Raw JSON:", JSON.stringify(panchang, null, 2));
