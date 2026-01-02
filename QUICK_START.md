# ActivityForYou - Quick Start Guide

## 🚀 What You Have

A complete, production-ready static web app for activity recommendations:

```
Frontend (GitHub Pages)          Backend (GitHub Actions)
├── index.html                   ├── generate-activities.yml
├── app.js                       └── generate_activities.py
├── style.css
└── data/
    ├── paris.json           ↑ Auto-generated daily
    ├── lyon.json            by Python script
    ├── marseille.json       that fetches weather
    ├── tokyo.json           and scores activities
    ├── new_york.json        using rule-based system
    └── sydney.json
```

## 📋 Included Components

### 1. **GitHub Actions Workflow** (`.github/workflows/generate-activities.yml`)
- Runs daily at 06:00 UTC
- Fetches real weather data from OpenWeatherMap API
- Generates/updates JSON files
- Auto-commits changes to repository

### 2. **Python Scoring Engine** (`scripts/generate_activities.py`)
A complete rule-based recommendation system with:
- **25 Activities** across 3 categories (outdoor, indoor, sports)
- **8 Scoring Rules** based on weather, temperature, time, day type, wind
- **Mock Data Support** for testing without API key
- **6 Cities** pre-configured (easy to add more)

### 3. **Frontend Application** (`docs/`)
- **index.html**: Beautiful responsive UI
- **app.js**: Smart data loader and renderer
- **style.css**: Modern gradient design, mobile-optimized
- **data/*.json**: Example files for all 6 cities

## 🎯 Rule-Based Scoring Examples

### Scenario: Rainy Day (Indoor Boost)
```
Base Activity Scores: [50-80]
Weather penalty (rainy): -40 for outdoor, +15 for indoor

BEFORE: Hiking (70), Cinema (70)
AFTER:  Hiking (30), Cinema (85) ← Rainy boost!
```

### Scenario: Sunny Summer Day (Outdoor Boost)
```
BEFORE: Beach (80), Museum (65)
AFTER:  Beach (105→100 capped), Museum (55) ← Sunny boost!
```

### Scenario: Cold Winter Evening (Indoor + Time Boost)
```
Temperature: -5°C
Time: Evening
Day: Weekday

Cinema: 70 + 15 (evening) + 10 (cold→indoor) = 95 ✓
Running: 80 - 20 (cold outdoor) = 60
```

## 🔧 Configuration

### API Key Setup
1. Get free key: https://openweathermap.org
2. Add to GitHub: Settings → Secrets → `OPENWEATHER_API_KEY`

### Add a City (3 steps)

**Step 1:** Edit `scripts/generate_activities.py`
```python
CITIES = {
    'paris': {'lat': 48.8566, 'lon': 2.3522},
    'london': {'lat': 51.5074, 'lon': -0.1278},  # ← Add here
}
```

**Step 2:** Edit `docs/index.html`
```html
<option value="london">London 🇬🇧</option>
```

**Step 3:** Run the workflow (Actions → Run workflow)

## 📊 Scoring System Deep Dive

### Activity Base Scores
```
High priority: Beach (80), Cycling (75), Cinema (70)
Medium priority: Hiking (70), Yoga (65), Café (60)
Low priority: Reading (50)
```

### Modifiers by Weather
```
Rainy:    Outdoor -40, Indoor +15
Sunny:    Outdoor +25, Indoor -10
Cloudy:   Outdoor -5
Wind>25:  Outdoor -10
```

### Modifiers by Temperature
```
< 0°C:    Water -30, Outdoor -20, Indoor +10
0-10°C:   Water -25, Outdoor -10
> 30°C:   Strenuous -15, Water +20
```

### Modifiers by Time of Day
```
Morning:    Yoga +20, Running +20
Afternoon:  Cycling +15, Beach +15, Park +15
Evening:    Cinema +20, Restaurant +20, Café +20
```

### Modifiers by Day Type
```
Weekend: Picnic +15, Hiking +15, Cinema +15, Restaurant +15
Weekday: Café +10, Yoga +10
```

## 📁 File Structure

```
ActivityForYou/
│
├── .github/workflows/
│   └── generate-activities.yml      ← Workflow config
│
├── docs/                             ← GitHub Pages root
│   ├── index.html                   ← Main UI
│   ├── app.js                       ← Frontend logic
│   ├── style.css                    ← Styling
│   │
│   └── data/                        ← Generated JSON
│       ├── paris.json               (weather + activities)
│       ├── lyon.json
│       ├── marseille.json
│       ├── tokyo.json
│       ├── new_york.json
│       └── sydney.json
│
├── scripts/
│   └── generate_activities.py       ← Python engine
│
└── README.md                        ← Full documentation
```

## 🎨 Frontend Features

| Feature | Details |
|---------|---------|
| **City Selector** | Dropdown with 6 emoji-labeled cities |
| **Weather Display** | Temperature, condition, wind speed, emoji icon |
| **Context Badges** | Time of day (morning/afternoon/evening) + weekday/weekend |
| **Activity Cards** | Top 10 results, color-coded by score |
| **Score Colors** | Green (70+), Orange (50-69), Red (<50) |
| **Reasons** | Why each activity got that score |
| **Responsive** | Works on desktop, tablet, mobile |
| **Update Time** | Shows when data was last generated |

## 💡 Real-World Examples

### Paris, Cloudy Morning (Weekday)
```json
{
  "weather": {"temperature": 8°C, "condition": "cloudy"},
  "context": {"time_of_day": "morning", "day_type": "weekday"},
  "top_activities": [
    {"name": "cafe", "score": 85},     // indoor boost
    {"name": "museum", "score": 80},   // indoor boost
    {"name": "yoga", "score": 78},     // morning boost
    {"name": "running", "score": 75},  // morning boost
  ]
}
```

### Sydney, Sunny Afternoon (Weekend)
```json
{
  "weather": {"temperature": 26°C, "condition": "sunny"},
  "context": {"time_of_day": "afternoon", "day_type": "weekend"},
  "top_activities": [
    {"name": "beach", "score": 95},     // sunny + hot + weekend
    {"name": "swimming", "score": 93},  // sunny + hot
    {"name": "picnic", "score": 88},    // sunny + weekend
    {"name": "cycling", "score": 85},   // sunny + afternoon
  ]
}
```

## 🔄 How Updates Work

```
Every Day at 06:00 UTC:
   ↓
GitHub Actions runs workflow
   ↓
Python script fetches live weather (6 API calls)
   ↓
Applies rule-based scoring
   ↓
Generates/updates 6 JSON files
   ↓
Commits changes to GitHub
   ↓
GitHub Pages automatically serves new JSON
   ↓
User's browser loads fresh data
```

## ⚙️ Customization Examples

### Change Update Time
Edit line 6 in `.github/workflows/generate-activities.yml`:
```yaml
- cron: '0 15 * * *'  # Change to 3 PM UTC
```

### Adjust Scoring (More Outdoor-Friendly)
Edit `scripts/generate_activities.py`, line ~80:
```python
if self.weather == 'rainy':
    score -= 30  # Changed from -40 (less penalty)
```

### Add Winter Activity
Edit `ACTIVITIES` dict in `scripts/generate_activities.py`:
```python
ACTIVITIES = {
    'outdoor': {
        'ice_skating': {'base_score': 70, 'description': 'Skate on ice'},
    }
}
```

## 📊 Performance

- **Zero Backend Costs** - GitHub Actions free tier ✓
- **Zero Database** - Pure static JSON ✓
- **API Calls** - 6/day (1,000 limit) ✓
- **Page Load Time** - <1 second (static site) ✓
- **Concurrent Users** - Unlimited (CDN) ✓

## 🐛 Testing the Scoring

### Test with Mock Data (No API Key Needed)
```bash
export OPENWEATHER_API_KEY=""  # Leave empty
python scripts/generate_activities.py
```

### Test with Real Data
```bash
export OPENWEATHER_API_KEY="your-key"
python scripts/generate_activities.py
```

### View Generated Data
```bash
cat docs/data/paris.json | python -m json.tool
```

## 🎁 What You Can Do Now

1. ✅ Push to GitHub and enable Pages
2. ✅ Add your OpenWeatherMap API key as a secret
3. ✅ Manual trigger the workflow (Actions → Run)
4. ✅ See live recommendations at yourdomain.github.io
5. ✅ Customize rules and activities
6. ✅ Add more cities
7. ✅ Change update schedule

---

**Questions?** Check README.md for full documentation.
