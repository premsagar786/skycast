# SkyCast - Django Weather App with Report Upload

A premium, beginner-friendly Django application that fetches real-time weather data and manages project reports.

## Features
- **Live Weather**: Search any city to get temperature, humidity, and more.
- **Search History**: Stores the last 5 searches in the database.
- **Report Management**: Upload and download project reports (PDF/DOCX).
- **Stunning UI**: Modern glassmorphism design with responsive layout.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install django requests
   ```

2. **Configure API Key**:
   - Open `main/views.py`.
   - Replace `"PLACEHOLDER_API_KEY"` with your [OpenWeatherMap API Key](https://openweathermap.org/api).

3. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the App**:
   Visit `http://127.0.0.1:8000` in your browser.

## Project Structure
- `main/`: Core application logic (Views, Models, Forms).
- `weather_project/`: Django project settings and routing.
- `media/`: Storage for uploaded report files.
- `templates/`: HTML structures with embedded CSS for premium styling.

## How it Works
- **Weather API**: Uses the `requests` library to fetch JSON data from OpenWeatherMap.
- **File Upload**: Uses Django's `FileField` and `form.save()` to securely handle uploads to the `media/reports/` directory.
- **History**: Automatically records every successful search to provide a quick reference.
