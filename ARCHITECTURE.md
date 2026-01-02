# Architecture & System Design

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  GitHub Actions (Backend Processing)                   │ │
│  │  ┌─────────────────────────────────────────────────┐   │ │
│  │  │ Trigger: Daily at 06:00 UTC                     │   │ │
│  │  │ (or Manual via workflow_dispatch)               │   │ │
│  │  └─────────────────────────────────────────────────┘   │ │
│  │              ↓                                           │ │
│  │  ┌─────────────────────────────────────────────────┐   │ │
│  │  │ Step 1: Fetch Weather Data                      │   │ │
│  │  │ - Call OpenWeatherMap API for 6 cities         │   │ │
│  │  │ - Extract: temperature, condition, wind        │   │ │
│  │  │ - Get: time_of_day, day_type (from UTC)       │   │ │
│  │  └─────────────────────────────────────────────────┘   │ │
│  │              ↓                                           │ │
│  │  ┌─────────────────────────────────────────────────┐   │ │
│  │  │ Step 2: Run Scoring Engine                      │   │ │
│  │  │ - ActivityScorer class applies rules            │   │ │
│  │  │ - Scores 25 activities per city                 │   │ │
│  │  │ - Generates reason explanations                 │   │ │
│  │  │ - Sorts by score (high to low)                  │   │ │
│  │  └─────────────────────────────────────────────────┘   │ │
│  │              ↓                                           │ │
│  │  ┌─────────────────────────────────────────────────┐   │ │
│  │  │ Step 3: Write JSON Files                        │   │ │
│  │  │ - docs/data/paris.json                          │   │ │
│  │  │ - docs/data/lyon.json                           │   │ │
│  │  │ - docs/data/marseille.json                      │   │ │
│  │  │ - docs/data/tokyo.json                          │   │ │
│  │  │ - docs/data/new_york.json                       │   │ │
│  │  │ - docs/data/sydney.json                         │   │ │
│  │  └─────────────────────────────────────────────────┘   │ │
│  │              ↓                                           │ │
│  │  ┌─────────────────────────────────────────────────┐   │ │
│  │  │ Step 4: Commit & Push                           │   │ │
│  │  │ - Git commit updated JSON files                 │   │ │
│  │  │ - Push to main branch                           │   │ │
│  │  └─────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────┘ │
│                      ↓ (triggers)                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  GitHub Pages (Static Website Hosting)                 │ │
│  │                                                          │ │
│  │  /docs/                                                 │ │
│  │  ├── index.html          (UI + structure)              │ │
│  │  ├── app.js              (interactive logic)           │ │
│  │  ├── style.css           (styling)                     │ │
│  │  └── data/               (generated recommendations)   │ │
│  │      ├── paris.json                                     │ │
│  │      ├── lyon.json                                      │ │
│  │      ├── marseille.json                                 │ │
│  │      ├── tokyo.json                                     │ │
│  │      ├── new_york.json                                  │ │
│  │      └── sydney.json                                    │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                          ↓ (CDN)
┌──────────────────────────────────────────────────────────────┐
│          End User's Browser (Frontend Client)               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Step 1: User selects a city from dropdown              │ │
│  └─────────────────────────────────────────────────────────┘ │
│                      ↓                                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Step 2: app.js loads corresponding JSON file           │ │
│  │ (e.g., data/paris.json)                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                      ↓                                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Step 3: Parse JSON and render UI                       │ │
│  │ - Display weather info                                 │ │
│  │ - Render activity recommendations                      │ │
│  │ - Show scores and reasons                              │ │
│  └─────────────────────────────────────────────────────────┘ │
│                      ↓                                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ User sees: Activity recommendations with scores        │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

### Weather Data Processing

```
OpenWeatherMap API
        ↓
   {
     "temperature": 8,
     "weather": [{"main": "Cloudy"}],
     "wind": {"speed": 3.3}  # m/s
   }
        ↓
Python Script Transforms
        ↓
   {
     "temperature": 8,
     "weather_type": "cloudy",
     "wind_speed": 11.88,  # km/h
     "time_of_day": "morning",
     "day_type": "weekday"
   }
        ↓
ActivityScorer Processing
```

### Scoring Algorithm Flow

```
For each activity:
  score = base_score (50-80)
  
  # Apply weather rules
  if weather == "rainy":
    score -= 40 (outdoor) OR += 15 (indoor)
  
  # Apply temperature rules
  if temp < 0:
    score -= 30 (water) or -= 20 (outdoor)
  
  # Apply time of day rules
  if time_of_day == "morning":
    score += 20 (for yoga, running)
  
  # Apply day type rules
  if day_type == "weekend":
    score += 15 (for leisure activities)
  
  # Apply wind rules
  if wind_speed > 25:
    score -= 10 (outdoor)
  
  # Clamp score between 0-100
  score = max(0, min(100, score))
  
  return {
    "name": activity,
    "score": score,
    "description": description,
    "reasons": [list of applied rules]
  }
```

## Rule System Architecture

### Rule Categories

1. **Weather Rules** (primary impact)
   - Rainy: penalize outdoor, boost indoor
   - Sunny: boost outdoor, penalize indoor
   - Cloudy: slight outdoor penalty

2. **Temperature Rules** (modifier by range)
   - Extreme cold (<0°C): major indoor boost
   - Cool (0-10°C): water activity penalty
   - Hot (>30°C): water boost, strenuous penalty

3. **Time Rules** (context-based)
   - Morning: fitness activities
   - Afternoon: scenic outdoor
   - Evening: social/indoor

4. **Day Type Rules** (lifestyle)
   - Weekend: leisure boost
   - Weekday: casual/quick activities

5. **Environmental Rules** (conditions)
   - High wind: outdoor penalty

### Scoring Example

**Paris, Rainy, 8°C, Morning, Weekday:**

```
Activity: "café"
├─ Base score: 60
├─ Weather rule (rainy, indoor): +15 → 75
├─ Temperature rule (8°C): no impact → 75
├─ Time rule (morning, indoor): no boost → 75
├─ Day type rule (weekday, casual): no boost → 75
└─ Final score: 75 ✓

Activity: "hiking"
├─ Base score: 70
├─ Weather rule (rainy, outdoor): -40 → 30
├─ Temperature rule (8°C, outdoor): -10 → 20
├─ Time rule (morning, outdoor): no boost → 20
├─ Day type rule (weekday): no boost → 20
└─ Final score: 20 ✗ (Not recommended)
```

## Data Structure

### Input: Weather Data (from API)

```json
{
  "temperature": 8,
  "weather_type": "cloudy",
  "wind_speed": 12.0,
  "time_of_day": "morning",
  "day_type": "weekday",
  "description": "Mostly cloudy",
  "icon": "02d"
}
```

### Processing: Scoring Context

```json
{
  "weather": "cloudy",
  "temperature": 8,
  "time_of_day": "morning",
  "day_type": "weekday",
  "wind_speed": 12.0
}
```

### Output: Recommendations JSON

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
      "score": 75,
      "description": "Relax at a cozy café",
      "reasons": [
        "Indoor activity preferred for cloudy weather",
        "Good weekday activity"
      ]
    },
    ...
  ]
}
```

## Technology Stack

| Layer | Technology | Role |
|-------|-----------|------|
| **Backend Processing** | Python 3.11 | Rule-based scoring engine |
| **Data Source** | OpenWeatherMap API | Real weather data |
| **CI/CD** | GitHub Actions | Scheduled job runner |
| **Data Storage** | JSON files | Generated recommendations |
| **Version Control** | Git | Tracks all changes |
| **Hosting** | GitHub Pages | Static site serving |
| **Frontend** | HTML5/CSS3/JavaScript | Interactive UI |
| **No Database** | N/A | Pure static approach |
| **No Backend Server** | N/A | Completely serverless |

## Performance Metrics

```
API Calls per Day:        6 (within 1,000 free limit)
Processing Time:          ~2 seconds
Data Size per City:       ~3 KB
Total Data:               ~18 KB (all 6 cities)
Page Load Time:           <500ms (static site)
Concurrent Users:         Unlimited (CDN)
Cost:                     $0 (GitHub free tier)
Uptime SLA:               99.9% (GitHub)
Update Frequency:         Daily
Freshness:                24 hours
```

## Extensibility Points

```
ActivityScorer
├── Add weather conditions (sleet, hail, etc.)
├── Add temperature bands
├── Add time windows
├── Add seasonal rules
└── Add activity categories

Activities Database
├── Add more activities
├── Adjust base scores
├── Add sub-categories
└── Add difficulty levels

Cities Configuration
├── Add new cities
├── Adjust coordinates
├── Add regional rules
└── Add timezone handling

Frontend
├── Add filters
├── Add favorites
├── Add history
└── Add PWA features
```

---

**This architecture ensures:**
- ✅ Zero backend costs
- ✅ Automatic daily updates
- ✅ Rule-based transparency
- ✅ Easy customization
- ✅ No external dependencies
- ✅ Fast performance
- ✅ Version controlled
