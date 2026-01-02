/**
 * Activity For You - Frontend Application
 * Loads and displays activity recommendations from JSON files
 */

const WEATHER_ICONS = {
    '01d': '☀️',
    '01n': '🌙',
    '02d': '⛅',
    '02n': '☁️',
    '03d': '☁️',
    '03n': '☁️',
    '04d': '☁️',
    '04n': '☁️',
    '09d': '🌧️',
    '09n': '🌧️',
    '10d': '🌧️',
    '10n': '🌧️',
    '11d': '⛈️',
    '11n': '⛈️',
    '13d': '❄️',
    '13n': '❄️',
    '50d': '🌫️',
    '50n': '🌫️',
};

class ActivityApp {
    constructor() {
        this.currentData = null;
        this.init();
    }

    init() {
        this.cacheElements();
        this.attachEventListeners();
    }

    cacheElements() {
        this.citySelect = document.getElementById('city-select');
        this.loading = document.getElementById('loading');
        this.errorMessage = document.getElementById('error-message');
        this.weatherCard = document.getElementById('weather-card');
        this.recommendationsContainer = document.getElementById('recommendations');
        this.activitiesList = document.getElementById('activities-list');
        
        // Weather card elements
        this.cityName = document.getElementById('city-name');
        this.temperature = document.getElementById('temperature');
        this.condition = document.getElementById('condition');
        this.wind = document.getElementById('wind');
        this.weatherIcon = document.getElementById('weather-icon');
        this.timeOfDay = document.getElementById('time-of-day');
        this.dayType = document.getElementById('day-type');
        this.lastUpdated = document.getElementById('last-updated');
    }

    attachEventListeners() {
        this.citySelect.addEventListener('change', (e) => {
            if (e.target.value) {
                this.loadCity(e.target.value);
            }
        });
    }

    async loadCity(cityName) {
        this.showLoading(true);
        this.hideError();

        try {
            const response = await fetch(`data/${cityName}.json`);
            
            if (!response.ok) {
                throw new Error(`Failed to load data for ${cityName}`);
            }

            this.currentData = await response.json();
            this.render();
        } catch (error) {
            this.showError(`Error loading city data: ${error.message}`);
            this.citySelect.value = '';
        } finally {
            this.showLoading(false);
        }
    }

    render() {
        this.renderWeatherCard();
        this.renderRecommendations();
        this.weatherCard.classList.remove('hidden');
        this.recommendationsContainer.classList.remove('hidden');
    }

    renderWeatherCard() {
        const data = this.currentData;
        const weather = data.weather;
        const context = data.context;

        this.cityName.textContent = this.formatCityName(data.city);
        this.temperature.textContent = `${weather.temperature}°C`;
        this.condition.textContent = weather.description;
        this.wind.textContent = `Wind: ${weather.wind_speed_kmh} km/h`;
        
        const iconEmoji = WEATHER_ICONS[weather.icon] || '🌤️';
        this.weatherIcon.textContent = iconEmoji;
        this.weatherIcon.alt = weather.description;

        this.timeOfDay.textContent = `⏰ ${context.time_of_day}`;
        this.dayType.textContent = `📅 ${context.day_type}`;

        const updatedDate = new Date(data.generated_at);
        const formattedDate = updatedDate.toLocaleDateString(undefined, {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            timeZone: 'UTC'
        });
        this.lastUpdated.textContent = `Last updated: ${formattedDate} UTC`;
    }

    renderRecommendations() {
        const recommendations = this.currentData.recommendations;
        this.activitiesList.innerHTML = '';

        recommendations.forEach((activity, index) => {
            const card = this.createActivityCard(activity, index);
            this.activitiesList.appendChild(card);
        });
    }

    createActivityCard(activity, index) {
        const card = document.createElement('div');
        card.className = 'activity-card';
        
        // Add score-based styling
        if (activity.score >= 70) {
            card.classList.add('high-score');
        } else if (activity.score >= 50) {
            card.classList.add('medium-score');
        }

        const scoreClass = activity.score >= 70 ? 'high' : activity.score >= 50 ? 'medium' : 'low';

        const reasonsHtml = activity.reasons
            .map(reason => `<li>${reason}</li>`)
            .join('');

        card.innerHTML = `
            <h4>${this.formatActivityName(activity.name)}</h4>
            <span class="activity-score ${scoreClass}">Score: ${activity.score}/100</span>
            <p class="activity-description">${activity.description}</p>
            <ul class="activity-reasons">
                ${reasonsHtml}
            </ul>
        `;

        return card;
    }

    formatCityName(name) {
        return name
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    formatActivityName(name) {
        return name
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    showLoading(show) {
        if (show) {
            this.loading.classList.remove('hidden');
            this.weatherCard.classList.add('hidden');
            this.recommendationsContainer.classList.add('hidden');
        } else {
            this.loading.classList.add('hidden');
        }
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorMessage.classList.remove('hidden');
    }

    hideError() {
        this.errorMessage.classList.add('hidden');
    }
}

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ActivityApp();
});
