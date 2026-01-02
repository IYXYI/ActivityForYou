# Usage Examples & Test Cases

## Example 1: Rainy Day in Lyon

### Input Weather Data
```python
{
    'city': 'lyon',
    'temperature': 6,
    'weather': 'rainy',
    'wind_speed': 15,
    'time_of_day': 'afternoon',
    'day_type': 'weekday'
}
```

### Scoring Process

```
Activity: "cinema"
├─ Base score: 70
├─ Rainy (indoor): +15 → 85
├─ Cool temp: no penalty for indoor → 85
├─ Afternoon: no boost for cinema → 85
├─ Weekday: no impact → 85
└─ Final: 85 ✓ TOP ACTIVITY

Activity: "hiking"
├─ Base score: 70
├─ Rainy (outdoor): -40 → 30
├─ Cool temp (outdoor): -10 → 20
├─ Afternoon: no boost → 20
├─ Weekday: no boost → 20
└─ Final: 20 ✗ NOT RECOMMENDED

Activity: "cafe"
├─ Base score: 60
├─ Rainy (indoor): +15 → 75
├─ Cool temp: no impact → 75
├─ Afternoon: no boost → 75
├─ Weekday: good activity +10 → 85 (tie with cinema)
└─ Final: 85 ✓ TOP ACTIVITY
```

### Result JSON
```json
{
  "recommendations": [
    {
      "name": "cinema",
      "score": 85,
      "description": "Watch a movie",
      "reasons": [
        "Indoor activity preferred for rainy weather",
        "Rainy weather reduces outdoor activities"
      ]
    },
    {
      "name": "cafe",
      "score": 85,
      "description": "Relax at a cozy café",
      "reasons": [
        "Indoor activity preferred for rainy weather",
        "Good weekday activity"
      ]
    },
    {
      "name": "museum",
      "score": 80,
      "description": "Explore art and culture",
      "reasons": [
        "Indoor activity preferred for rainy weather"
      ]
    },
    {
      "name": "hiking",
      "score": 20,
      "description": "Explore nature trails",
      "reasons": [
        "Rainy weather reduces outdoor activities",
        "Cool temperature (6°C)"
      ]
    }
  ]
}
```

---

## Example 2: Sunny Summer Day in Sydney

### Input Weather Data
```python
{
    'city': 'sydney',
    'temperature': 26,
    'weather': 'sunny',
    'wind_speed': 14,
    'time_of_day': 'afternoon',
    'day_type': 'weekend'
}
```

### Scoring Process

```
Activity: "beach"
├─ Base score: 80
├─ Sunny (outdoor): +25 → 105
├─ Hot (25-30°C, water): +20 → 125 → capped at 100
├─ Afternoon: +15 → 100 (already at cap)
├─ Weekend: +15 → 100 (already at cap)
└─ Final: 100 ✓ MAXIMUM SCORE

Activity: "swimming"
├─ Base score: 80
├─ Sunny (outdoor): +25 → 105
├─ Hot (water): +20 → 125 → capped at 100
├─ Afternoon: +15 → 100 (already at cap)
└─ Final: 100 ✓ MAXIMUM SCORE

Activity: "hiking"
├─ Base score: 70
├─ Sunny (outdoor): +25 → 95
├─ Hot (strenuous): -15 → 80
├─ Weekend: +15 → 95
└─ Final: 95 ✓ HIGHLY RECOMMENDED

Activity: "museum"
├─ Base score: 65
├─ Sunny (indoor): -10 → 55
├─ Weekend: no boost → 55
└─ Final: 55 ✗ LESS ATTRACTIVE (nice weather outside)

Activity: "reading"
├─ Base score: 50
├─ Sunny (indoor): -10 → 40
└─ Final: 40 ✗ NOT RECOMMENDED
```

### Result JSON
```json
{
  "recommendations": [
    {
      "name": "beach",
      "score": 100,
      "description": "Relax and swim at the beach",
      "reasons": [
        "Perfect sunny weather for outdoor activities",
        "Hot weather (26°C) perfect for water activities",
        "Great afternoon activity",
        "Perfect weekend activity"
      ]
    },
    {
      "name": "swimming",
      "score": 100,
      "description": "Swim at a pool or beach",
      "reasons": [
        "Perfect sunny weather for outdoor activities",
        "Hot weather (26°C) perfect for water activities",
        "Great afternoon activity"
      ]
    },
    {
      "name": "hiking",
      "score": 95,
      "description": "Explore nature trails",
      "reasons": [
        "Perfect sunny weather for outdoor activities",
        "Perfect weekend activity"
      ]
    },
    {
      "name": "museum",
      "score": 55,
      "description": "Explore art and culture",
      "reasons": [
        "Nice weather available outside"
      ]
    }
  ]
}
```

---

## Example 3: Cold Snowy Evening in New York

### Input Weather Data
```python
{
    'city': 'new_york',
    'temperature': -5,
    'weather': 'rainy',  # Light snow
    'wind_speed': 20,
    'time_of_day': 'evening',
    'day_type': 'weekday'
}
```

### Scoring Process

```
Activity: "cinema"
├─ Base score: 70
├─ Rainy (indoor): +15 → 85
├─ Cold (indoor): +10 → 95
├─ Evening (cinema): +20 → 115 → capped at 100
└─ Final: 100 ✓ BEST CHOICE

Activity: "restaurant"
├─ Base score: 75
├─ Rainy (indoor): +15 → 90
├─ Cold (indoor): +10 → 100
├─ Evening (restaurant): +20 → 120 → capped at 100
└─ Final: 100 ✓ BEST CHOICE

Activity: "cafe"
├─ Base score: 60
├─ Rainy (indoor): +15 → 75
├─ Cold (indoor): +10 → 85
├─ Evening (cafe): +20 → 105 → capped at 100
└─ Final: 100 ✓ BEST CHOICE

Activity: "running"
├─ Base score: 80
├─ Rainy (outdoor): -40 → 40
├─ Cold (outdoor): -20 → 20
├─ Evening (outdoor): -15 → 5
└─ Final: 5 ✗ STRONGLY NOT RECOMMENDED

Activity: "beach"
├─ Base score: 80
├─ Rainy (outdoor): -40 → 40
├─ Cold (water): -30 → 10
├─ Wind (high): -10 → 0
└─ Final: 0 ✗ DO NOT RECOMMEND
```

### Result JSON
```json
{
  "recommendations": [
    {
      "name": "cinema",
      "score": 100,
      "description": "Watch a movie",
      "reasons": [
        "Indoor activity preferred for rainy weather",
        "Popular evening activity",
        "Cold weather makes indoor activities attractive"
      ]
    },
    {
      "name": "restaurant",
      "score": 100,
      "description": "Dine at a local restaurant",
      "reasons": [
        "Indoor activity preferred for rainy weather",
        "Popular evening activity"
      ]
    },
    {
      "name": "cafe",
      "score": 85,
      "description": "Relax at a cozy café",
      "reasons": [
        "Indoor activity preferred for rainy weather",
        "Popular evening activity",
        "Good weekday activity"
      ]
    },
    {
      "name": "running",
      "score": 5,
      "description": "Morning or evening jog",
      "reasons": [
        "Rainy weather reduces outdoor activities",
        "Very cold (-5°C) for strenuous activities",
        "Limited daylight for outdoor activities"
      ]
    },
    {
      "name": "beach",
      "score": 0,
      "description": "Relax and swim at the beach",
      "reasons": [
        "Rainy weather reduces outdoor activities",
        "Very cold (-5°C) for water activities",
        "High wind speed (20 km/h)"
      ]
    }
  ]
}
```

---

## Example 4: Cool Sunny Morning in Paris

### Input Weather Data
```python
{
    'city': 'paris',
    'temperature': 8,
    'weather': 'sunny',
    'wind_speed': 12,
    'time_of_day': 'morning',
    'day_type': 'weekday'
}
```

### Scoring Process

```
Activity: "running"
├─ Base score: 80
├─ Sunny (outdoor): +25 → 105 → capped at 100
├─ Cool temp (outdoor): -10 → 90
├─ Morning (running): +20 → 110 → capped at 100
└─ Final: 100 ✓ PERFECT MORNING JOG

Activity: "yoga"
├─ Base score: 65
├─ Sunny (outdoor): +25 → 90
├─ Morning (yoga): +20 → 110 → capped at 100
└─ Final: 100 ✓ PERFECT MORNING YOGA

Activity: "hiking"
├─ Base score: 70
├─ Sunny (outdoor): +25 → 95
├─ Cool temp (outdoor): -10 → 85
└─ Final: 85 ✓ GOOD ACTIVITY

Activity: "cycling"
├─ Base score: 75
├─ Sunny (outdoor): +25 → 100
├─ Cool temp (outdoor): -10 → 90
└─ Final: 90 ✓ GOOD ACTIVITY

Activity: "cafe"
├─ Base score: 60
├─ Sunny (indoor): -10 → 50
├─ Weekday (casual): +10 → 60
└─ Final: 60 ✗ LESS ATTRACTIVE (nice weather outside)

Activity: "cinema"
├─ Base score: 70
├─ Sunny (indoor): -10 → 60
└─ Final: 60 ✗ NOT RECOMMENDED
```

### Result JSON
```json
{
  "recommendations": [
    {
      "name": "running",
      "score": 100,
      "description": "Morning or evening jog",
      "reasons": [
        "Perfect sunny weather for outdoor activities",
        "Ideal morning activity"
      ]
    },
    {
      "name": "yoga",
      "score": 100,
      "description": "Yoga session",
      "reasons": [
        "Ideal morning activity"
      ]
    },
    {
      "name": "cycling",
      "score": 90,
      "description": "Ride through the city or countryside",
      "reasons": [
        "Perfect sunny weather for outdoor activities"
      ]
    },
    {
      "name": "hiking",
      "score": 85,
      "description": "Explore nature trails",
      "reasons": [
        "Perfect sunny weather for outdoor activities"
      ]
    },
    {
      "name": "cafe",
      "score": 60,
      "description": "Relax at a cozy café",
      "reasons": [
        "Nice weather available outside",
        "Good weekday activity"
      ]
    }
  ]
}
```

---

## Scoring Rules Reference

### Weather Modifiers
```
Rainy Weather:
  - Outdoor activities: -40
  - Indoor activities: +15
  
Sunny Weather:
  - Outdoor activities: +25
  - Indoor activities: -10
  
Cloudy Weather:
  - Outdoor activities: -5
```

### Temperature Modifiers
```
Very Cold (< 0°C):
  - Water activities: -30
  - Outdoor activities: -20
  - Indoor activities: +10
  
Cool (0°C to 10°C):
  - Water activities: -25
  - Outdoor activities: -10
  
Hot (> 30°C):
  - Strenuous activities: -15
  - Water activities: +20
```

### Time of Day Modifiers
```
Morning (6 AM - 12 PM):
  - Yoga: +20
  - Running: +20
  
Afternoon (12 PM - 6 PM):
  - Cycling: +15
  - Beach: +15
  - Park walk: +15
  
Evening (6 PM - 6 AM):
  - Cinema: +20
  - Restaurant: +20
  - Café: +20
  - Outdoor: -15
```

### Day Type Modifiers
```
Weekend:
  - Picnic: +15
  - Hiking: +15
  - Cinema: +15
  - Restaurant: +15
  
Weekday:
  - Café: +10
  - Yoga: +10
```

### Environmental Modifiers
```
High Wind (> 25 km/h):
  - Outdoor activities: -10
```

---

## Testing Scenarios

### Test Case 1: Perfect Outdoor Day
**Conditions:** Sunny, 22°C, Afternoon, Weekend, Low wind

**Expected:** Beach, Cycling, Picnic, Hiking dominate (scores 85-95)

### Test Case 2: Indoor Day
**Conditions:** Rainy, 5°C, Evening, Weekday, Moderate wind

**Expected:** Cinema, Restaurant, Café, Gaming dominate (scores 80-100)

### Test Case 3: Morning Fitness
**Conditions:** Sunny, 10°C, Morning, Weekday, Light wind

**Expected:** Running, Yoga top choices (scores 95-100)

### Test Case 4: Extreme Cold
**Conditions:** Snowy, -10°C, Evening, Weekday, High wind

**Expected:** Only indoor activities recommended (scores 100+)

### Test Case 5: Hot Summer
**Conditions:** Sunny, 35°C, Afternoon, Weekend, Light wind

**Expected:** Beach, Swimming top (scores 95-100), Strenuous outdoor low

---

## Customization Examples

### Make Weather More Important
Edit `generate_activities.py`, change weather penalty:
```python
# Original
if self.weather == 'rainy':
    score -= 40  # Change to:
    score -= 60  # Much stronger penalty
```

### Boost Weekend Activities More
```python
# Original
if self.day_type == 'weekend':
    score += 15  # Change to:
    score += 30  # Double the boost
```

### Add Temperature-Based Seasonal Activities
```python
ACTIVITIES['seasonal'] = {
    'ice_skating': {
        'base_score': 75,
        'description': 'Ice skating rink',
    },
    'skiing': {
        'base_score': 85,
        'description': 'Ski resort',
    },
}

# In score_activity():
if self.temp < -5:
    if activity_name == 'ice_skating':
        score += 20
```

### Add More Granular Time Bands
```python
# Instead of just morning/afternoon/evening:
def get_current_time_of_day():
    hour = datetime.utcnow().hour
    if 5 <= hour < 8:
        return 'early_morning'
    elif 8 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 15:
        return 'early_afternoon'
    # ... etc
```

---

## Performance Notes

```
Scoring Time per City:
  - 25 activities × 8-12 rules each = ~300 rule evaluations
  - Processing: < 100ms per city
  - Total for 6 cities: ~600ms
  
API Response Time:
  - OpenWeatherMap: 200-500ms per call
  - 6 cities sequentially: 1.2-3s total
  
JSON Size:
  - Per city: 2-4 KB
  - 6 cities: 12-24 KB total
  - Easily cacheable by CDN
```
