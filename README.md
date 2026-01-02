# Activity For You 🎯

A fully serverless, static web app hosted on GitHub Pages that suggests activities based on weather conditions in your city. **No backend server needed!**

## Architecture Overview

```
┌─────────────────────────────────────────┐
│  GitHub Actions (Daily Schedule)        │
│  - Fetch weather from OpenWeatherMap    │
│  - Run rule-based scoring engine        │
│  - Generate city JSON files             │
│  - Commit to repository                 │
└─────────────────────────────────────────┘
                    ↓
        (Commits generated JSON files)
                    ↓
┌─────────────────────────────────────────┐
│  GitHub Pages (Static Hosting)          │
│  - index.html                           │
│  - app.js                               │
│  - style.css                            │
│  - data/paris.json, lyon.json, etc.     │
└─────────────────────────────────────────┘
                    ↓
            (Browser requests)
                    ↓
┌─────────────────────────────────────────┐
│  User Browser (Frontend)                │
│  - Select a city                        │
│  - Load JSON file                       │
│  - Display recommendations              │
└─────────────────────────────────────────┘
```

## Project Structure

```
ActivityForYou/
├── .github/
│   └── workflows/
│       └── generate-activities.yml    # GitHub Actions workflow
├── docs/                              # GitHub Pages root
│   ├── index.html                     # Frontend UI
│   ├── app.js                         # Frontend logic
│   ├── style.css                      # Styling
│   └── data/
│       ├── paris.json                 # Generated activity data
│       ├── lyon.json
│       ├── marseille.json
│       ├── tokyo.json
│       ├── new_york.json
│       └── sydney.json
├── scripts/
│   └── generate_activities.py         # Activity recommendation engine
└── README.md                          # This file
```

## How It Works

### 1. GitHub Actions Workflow

Runs daily at 06:00 UTC to:
- Fetch current weather for predefined cities using OpenWeatherMap API
- Pass weather data to the Python scoring engine
- Generate/update JSON files with activity recommendations
- Commit changes back to the repository

**Trigger:** Schedule-based (daily) or manual via `workflow_dispatch`

### 2. Rule-Based Scoring Engine

A Python system that scores activities based on:

#### Input Factors
- **Weather**: sunny, rainy, cloudy
- **Temperature**: numeric value in Celsius
- **Time of Day**: morning (6-12), afternoon (12-18), evening (18-6)
- **Day Type**: weekday or weekend
- **Wind Speed**: in km/h

#### Scoring Rules

| Factor | Impact | Example |
|--------|--------|---------|
| **Rainy weather** | -40 outdoor, +15 indoor | Prefer cinema, museum, café |
| **Sunny weather** | +25 outdoor, -10 indoor | Boost beach, hiking, cycling |
| **Cloudy weather** | -5 outdoor | Slightly reduce appeal |
| **Cold (<0°C)** | -30 water, -20 outdoor, +10 indoor | Shift to indoor activities |
| **Cool (0-10°C)** | -25 water, -10 outdoor | Penalize water activities |
| **Hot (>30°C)** | -15 strenuous, +20 water | Boost swimming, reduce hiking |
| **Morning** | +20 yoga/running | Ideal for fitness |
| **Afternoon** | +15 cycling/park/beach | Scenic outdoor activities |
| **Evening** | +20 cinema/restaurant/café | Social/indoor activities |
| **Weekend** | +15 leisure | Boost picnic, hiking, cinema |
| **High wind (>25 km/h)** | -10 outdoor | Reduce outdoor appeal |

#### Activity Categories

**Outdoor:** hiking, picnic, cycling, beach, park_walk  
**Indoor:** cinema, museum, restaurant, café, gaming, reading  
**Sports:** running, tennis, swimming, yoga  

### 3. JSON Output Format

```json
{
  "city": "paris",
  "generated_at": "2025-01-02T10:00:00Z",
  "weather": {
    "temperature": 8,
    "condition": "cloudy",
    "description": "Mostly cloudy",
    "wind_speed_kmh": 12.0,
    "icon": "02d"
  },
  "context": {
    "time_of_day": "morning",
    "day_type": "weekday"
  },
  "recommendations": [
    {
      "name": "cafe",
      "score": 85,
      "description": "Relax at a cozy café",
      "reasons": [
        "Indoor activity preferred for cloudy weather",
        "Popular morning activity"
      ]
    }
  ]
}
```

### 4. Frontend Features

- 🌍 City selector dropdown
- 🌡️ Current weather display with icon
- ⏰ Time of day and day type badges
- 🎯 Top 10 activities ranked by score
- 🎨 Color-coded cards (green = high, orange = medium, red = low)
- 📱 Responsive mobile-friendly design
- 🔄 Last update timestamp

**Key: No API calls from frontend** - Everything loaded from static JSON files!

## Setup Instructions

### 1. Fork/Clone This Repository

```bash
git clone https://github.com/YOUR_USERNAME/ActivityForYou.git
cd ActivityForYou
```

### 2. Get OpenWeatherMap API Key

1. Sign up at [openweathermap.org](https://openweathermap.org)
2. Get a free API key (no CC required)
3. Store as GitHub secret:
   - Settings → Secrets and variables → Actions
   - Create: `OPENWEATHER_API_KEY`

### 3. Enable GitHub Pages

1. Settings → Pages
2. Source: `Deploy from a branch`
3. Branch: `main`, Folder: `/docs`
4. Save

Site will be live at: `https://YOUR_USERNAME.github.io/ActivityForYou`

### 4. Test the Workflow

1. Go to Actions tab
2. Select "Generate Activity Recommendations"
3. Click "Run workflow"

## Customization

### Add More Cities

Edit `scripts/generate_activities.py`:

```python
CITIES = {
    'paris': {'lat': 48.8566, 'lon': 2.3522},
    'london': {'lat': 51.5074, 'lon': -0.1278},  # Add new
}
```

Add to `docs/index.html`:
```html
<option value="london">London 🇬🇧</option>
```

### Modify Scoring Rules

Edit `ActivityScorer` class in `scripts/generate_activities.py`:

```python
if self.weather == 'rainy':
    score -= 40  # Adjust this
```

### Add More Activities

Extend `ACTIVITIES` dictionary:

```python
ACTIVITIES = {
    'outdoor': {
        'rock_climbing': {'base_score': 80, 'description': 'Scale a rock wall'},
    }
}
```

### Change Update Schedule

Edit `.github/workflows/generate-activities.yml`:

```yaml
on:
  schedule:
    - cron: '0 15 * * *'  # 3 PM UTC daily
```

## Local Testing

### Generate JSON Files

```bash
pip install requests
export OPENWEATHER_API_KEY='your-api-key'
python scripts/generate_activities.py
```

### Serve Frontend

```bash
cd docs
python -m http.server 8000
# Open http://localhost:8000
```

## API Costs

**OpenWeatherMap Free Tier:** 1,000 calls/day

- 6 cities × 1 call/day = 6 calls ✅
- Free tier, no CC required

## Advantages

✅ **Zero Backend Costs** - GitHub Pages & Actions free  
✅ **No Uptime Issues** - Completely serverless  
✅ **No Frontend API Calls** - Pre-computed data  
✅ **No Database** - Pure static files  
✅ **Simple Deploy** - GitHub native  
✅ **Easy Customize** - Python + JavaScript  
✅ **Version Control** - Full Git tracking  
✅ **No Authentication** - Public weather data  

## Limitations

- Updates on schedule (not real-time)
- OpenWeatherMap: 1,000 calls/day free tier
- Rule-based (not AI-powered)
- Limited to predefined cities

## Example Scenarios

**Sunny Summer (30°C, Afternoon, Weekend)**  
→ Beach, Swimming, Picnic, Cycling

**Rainy Weekday (8°C, Morning)**  
→ Café, Cinema, Museum, Reading

**Cool Sunny Fall (5°C, Morning)**  
→ Running, Yoga, Park Walk, Hiking

## Troubleshooting

### JSON not updating?
- Check Actions tab for errors
- Verify `OPENWEATHER_API_KEY` secret is set
- Review Python script output in logs

### Frontend not loading?
- Open DevTools (F12) → Console
- Check for 404 errors
- Verify GitHub Pages enabled for `/docs`

### "Failed to load data"?
- Ensure JSON files in `docs/data/`
- Match filename with city selector value
- Check UTF-8 encoding

## Future Enhancements

- [ ] User location detection
- [ ] Favorite cities
- [ ] Activity filters
- [ ] 7-day forecast
- [ ] Social sharing
- [ ] PWA/offline support
- [ ] Multi-language

## License

MIT License

---

**Built with ❤️ using GitHub Pages + Actions (No Backend!)**
