This is ScrapBridge project backend part written in Django, there is all the api's and model structure needed to run our Scrapbridge project
To run the project in your device, please download both the frontend and backend respositery.
Frontend repositery link : https://github.com/shivam2419/Scrapbridge-frontend/

# Platform overview
https://drive.google.com/file/d/1bkjLHavZuKS4tNPbYORWf5RfANMBBmTS/view?usp=sharing
# Live at : https://scrapbridge-api.onrender.com/
# ScrapBridge ♻️

**ScrapBridge** is a web-based platform that connects households with certified scrap collectors. The goal is to make recycling easier, smarter, and more accessible by allowing users to schedule pickups, classify scrap, and view real-time scrap prices.

---

## 🌟 Features

- 🔐 User and Collector Login System
- 🗓️ Schedule Scrap Pickups
- 📸 Scrap Image Classification (AI-powered)
- 📍 Location-based Pickup Assignment (Leaflet.js)
- 🔔 Real-time Notifications (via RapidAPI)
- 💸 Live Scrap Pricing and Payments (Razorpay)
- 📦 Collector Dashboard with Order Management

---

## 🧠 Why ScrapBridge?

Managing household scrap is often a hassle — people don’t know its value or how to dispose of it. ScrapBridge offers:
- Awareness about recyclable items
- Seamless pickup scheduling
- A step toward sustainable living 🌍

---

## 🛠 Tech Stack

| Frontend | Backend | ML | Other Services |
|----------|---------|----|----------------|
| React.js | Django  | TensorFlow / Keras (for classification) | Leaflet, Razorpay, RapidAPI, SQLite |

---

## 🚀 How to Run Locally

1. Set up the backend:
```bash
git clone https://github.com/your-username/Scrapbridge-backend.git
cd Scrapbridge-backend

cd EWaste

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```
2. Set up the frontend
```bash
git clone https://github.com/your-username/Scrapbridge-frontend.git
cd Scrapbridge-frontend

cd frontend

npm install
npm start
```

To use services like *Razorpay*, *OAuth login* that requires API key, there you have to use your own api key. (Write them in settings.py or .env file)
