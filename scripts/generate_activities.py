#!/usr/bin/env python3
"""
Activity Recommendation Generator
Fetches weather data and generates activity suggestions based on rule-based scoring.
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

# Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
OUTPUT_DIR = Path('docs/data')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Cities to generate recommendations for
CITIES = {
    'paris': {'lat': 48.8566, 'lon': 2.3522},
    'lyon': {'lat': 45.7640, 'lon': 4.8357},
    'marseille': {'lat': 43.2965, 'lon': 5.3698},
    'tokyo': {'lat': 35.6762, 'lon': 139.6503},
    'new_york': {'lat': 40.7128, 'lon': -74.0060},
    'sydney': {'lat': -33.8688, 'lon': 151.2093},
}

# Activity database
ACTIVITIES = {
    'outdoor': {
        'hiking': {'base_score': 70, 'description': 'Explore nature trails'},
        'picnic': {'base_score': 65, 'description': 'Enjoy outdoor meal with friends'},
        'cycling': {'base_score': 75, 'description': 'Ride through the city or countryside'},
        'beach': {'base_score': 80, 'description': 'Relax and swim at the beach'},
        'park_walk': {'base_score': 60, 'description': 'Stroll through a scenic park'},
    },
    'indoor': {
        'cinema': {'base_score': 70, 'description': 'Watch a movie'},
        'museum': {'base_score': 65, 'description': 'Explore art and culture'},
        'restaurant': {'base_score': 75, 'description': 'Dine at a local restaurant'},
        'cafe': {'base_score': 60, 'description': 'Relax at a cozy café'},
        'gaming': {'base_score': 70, 'description': 'Video games or board games'},
        'reading': {'base_score': 50, 'description': 'Read at home or library'},
    },
    'sports': {
        'running': {'base_score': 80, 'description': 'Morning or evening jog'},
        'tennis': {'base_score': 75, 'description': 'Play tennis with friends'},
        'swimming': {'base_score': 80, 'description': 'Swim at a pool or beach'},
        'yoga': {'base_score': 65, 'description': 'Yoga session'},
    }
}

class ActivityScorer:
    """Rule-based activity scoring system"""
    
    def __init__(self, weather_data):
        self.weather = weather_data['weather_type']
        self.temp = weather_data['temperature']
        self.time_of_day = weather_data['time_of_day']
        self.day_type = weather_data['day_type']
        self.wind_speed = weather_data.get('wind_speed', 0)
    
    def score_activity(self, activity_name, category):
        """Calculate score for an activity based on weather rules"""
        activity = ACTIVITIES[category][activity_name]
        score = activity['base_score']
        reasons = []
        
        # Weather rules
        if self.weather == 'rainy':
            if category == 'outdoor':
                score -= 40
                reasons.append("Rainy weather reduces outdoor activities")
            else:
                score += 15
                reasons.append("Indoor activity preferred for rainy weather")
        
        elif self.weather == 'sunny':
            if category == 'outdoor':
                score += 25
                reasons.append("Perfect sunny weather for outdoor activities")
            else:
                score -= 10
                reasons.append("Nice weather available outside")
        
        elif self.weather == 'cloudy':
            if category == 'outdoor':
                score -= 5
                reasons.append("Cloudy weather slightly reduces outdoor appeal")
        
        # Temperature rules
        if self.temp < 0:
            if activity_name in ['beach', 'picnic', 'cycling']:
                score -= 30
                reasons.append(f"Too cold ({self.temp}°C) for this activity")
            elif category == 'outdoor':
                score -= 20
                reasons.append(f"Cold temperature ({self.temp}°C)")
            else:
                score += 10
                reasons.append(f"Cold weather makes indoor activities attractive")
        
        elif self.temp < 10:
            if activity_name in ['beach', 'swimming']:
                score -= 25
                reasons.append(f"Cold ({self.temp}°C) for water activities")
            elif category == 'outdoor':
                score -= 10
                reasons.append(f"Cool temperature ({self.temp}°C)")
        
        elif self.temp > 30:
            if activity_name in ['hiking', 'running']:
                score -= 15
                reasons.append(f"Very hot ({self.temp}°C) for strenuous activities")
            elif activity_name == 'beach' or activity_name == 'swimming':
                score += 20
                reasons.append(f"Hot weather ({self.temp}°C) perfect for water activities")
        
        # Time of day rules
        if self.time_of_day == 'morning':
            if activity_name in ['running', 'yoga']:
                score += 20
                reasons.append("Ideal morning activity")
        
        elif self.time_of_day == 'afternoon':
            if activity_name in ['cycling', 'park_walk', 'beach']:
                score += 15
                reasons.append("Great afternoon activity")
        
        elif self.time_of_day == 'evening':
            if activity_name in ['cinema', 'restaurant', 'cafe']:
                score += 20
                reasons.append("Popular evening activity")
            elif category == 'outdoor':
                score -= 15
                reasons.append("Limited daylight for outdoor activities")
        
        # Day type rules
        if self.day_type == 'weekend':
            if activity_name in ['picnic', 'hiking', 'cinema', 'restaurant']:
                score += 15
                reasons.append("Perfect weekend activity")
        else:  # weekday
            if activity_name in ['cafe', 'quick_walk', 'yoga']:
                score += 10
                reasons.append("Good weekday activity")
        
        # Wind speed rules
        if self.wind_speed > 25:
            if category == 'outdoor':
                score -= 10
                reasons.append(f"High wind speed ({self.wind_speed} km/h)")
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        return {
            'name': activity_name,
            'score': score,
            'description': activity['description'],
            'reasons': reasons if reasons else ['Suitable for current weather']
        }
    
    def get_recommendations(self):
        """Get all activities sorted by score"""
        recommendations = []
        
        for category, activities in ACTIVITIES.items():
            for activity_name in activities:
                rec = self.score_activity(activity_name, category)
                recommendations.append(rec)
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations


def get_current_time_of_day():
    """Determine current time of day (UTC)"""
    hour = datetime.utcnow().hour
    if 6 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 18:
        return 'afternoon'
    else:
        return 'evening'


def get_day_type():
    """Determine if today is weekday or weekend"""
    weekday = datetime.utcnow().weekday()
    return 'weekend' if weekday >= 5 else 'weekday'


def fetch_weather(city_name, lat, lon):
    """Fetch weather data from OpenWeatherMap API"""
    if not OPENWEATHER_API_KEY:
        print(f"Warning: OPENWEATHER_API_KEY not set, using mock data for {city_name}")
        return get_mock_weather(city_name)
    
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Map OpenWeather conditions to our categories
        weather_main = data['weather'][0]['main'].lower()
        if 'rain' in weather_main or 'drizzle' in weather_main:
            weather_type = 'rainy'
        elif 'clear' in weather_main or 'sunny' in weather_main:
            weather_type = 'sunny'
        else:
            weather_type = 'cloudy'
        
        return {
            'temperature': round(data['main']['temp']),
            'weather_type': weather_type,
            'wind_speed': data['wind']['speed'] * 3.6,  # Convert m/s to km/h
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
        }
    except Exception as e:
        print(f"Error fetching weather for {city_name}: {e}")
        return get_mock_weather(city_name)


def get_mock_weather(city_name):
    """Return mock weather data for testing"""
    mock_data = {
        'paris': {'temperature': 8, 'weather_type': 'cloudy', 'wind_speed': 12, 'description': 'Mostly cloudy', 'icon': '02d'},
        'lyon': {'temperature': 6, 'weather_type': 'rainy', 'wind_speed': 15, 'description': 'Light rain', 'icon': '10d'},
        'marseille': {'temperature': 12, 'weather_type': 'sunny', 'wind_speed': 8, 'description': 'Clear sky', 'icon': '01d'},
        'tokyo': {'temperature': 5, 'weather_type': 'cloudy', 'wind_speed': 10, 'description': 'Overcast', 'icon': '04d'},
        'new_york': {'temperature': 2, 'weather_type': 'rainy', 'wind_speed': 20, 'description': 'Light snow', 'icon': '13d'},
        'sydney': {'temperature': 26, 'weather_type': 'sunny', 'wind_speed': 14, 'description': 'Clear sky', 'icon': '01d'},
    }
    return mock_data.get(city_name, {'temperature': 15, 'weather_type': 'cloudy', 'wind_speed': 10, 'description': 'Unknown', 'icon': '04d'})


def generate_city_data(city_name, lat, lon):
    """Generate activity recommendations for a city"""
    weather = fetch_weather(city_name, lat, lon)
    
    weather_with_time = {
        **weather,
        'time_of_day': get_current_time_of_day(),
        'day_type': get_day_type(),
    }
    
    scorer = ActivityScorer(weather_with_time)
    recommendations = scorer.get_recommendations()
    
    return {
        'city': city_name,
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'weather': {
            'temperature': weather['temperature'],
            'condition': weather['weather_type'],
            'description': weather['description'],
            'wind_speed_kmh': round(weather['wind_speed'], 1),
        },
        'context': {
            'time_of_day': weather_with_time['time_of_day'],
            'day_type': weather_with_time['day_type'],
        },
        'recommendations': recommendations[:10],  # Top 10 activities
    }


def main():
    """Main function to generate all city data"""
    print("Starting activity recommendation generation...")
    
    for city_name, coords in CITIES.items():
        print(f"Generating data for {city_name}...")
        
        try:
            city_data = generate_city_data(city_name, coords['lat'], coords['lon'])
            
            output_file = OUTPUT_DIR / f"{city_name}.json"
            with open(output_file, 'w') as f:
                json.dump(city_data, f, indent=2)
            
            print(f"  ✓ Saved to {output_file}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("Done!")


if __name__ == '__main__':
    main()
