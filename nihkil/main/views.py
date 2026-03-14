import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SearchHistory, ProjectReport
from .forms import ReportForm

# Your OpenWeatherMap API key
API_KEY = "f03538f0348002396d04c6595020868c"

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code == 200:
            return {
                'city': data['name'],
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'error': None
            }
        else:
            return {'error': data.get('message', 'City not found')}
    except requests.exceptions.RequestException:
        return {'error': 'Network error occurred'}

def index(request):
    weather_data = None
    city = request.POST.get('city', '').strip() if request.method == 'POST' else request.GET.get('city', '').strip()
    
    if city:
        weather_res = fetch_weather(city)
        if weather_res['error']:
            messages.error(request, weather_res['error'])
        else:
            weather_data = weather_res
            # Update or create to ensure the city moves to the top of "Recent Items"
            obj, created = SearchHistory.objects.update_or_create(
                city_name=weather_res['city'],
                defaults={
                    'temperature': weather_res['temp'],
                    'humidity': weather_res['humidity'],
                    'pressure': weather_res['pressure'],
                    'description': weather_res['description'],
                    'icon': weather_res['icon'],
                }
            )
            if not created:
                from django.utils import timezone
                obj.searched_at = timezone.now()
                obj.save()

            # Maintain strictly 4 records
            history_ids = SearchHistory.objects.all().order_by('-searched_at').values_list('id', flat=True)[:4]
            SearchHistory.objects.exclude(id__in=history_ids).delete()
    elif request.method == 'POST' and 'search_city' in request.POST:
        messages.warning(request, "Please enter a city name")



    if request.method == 'POST' and 'upload_report' in request.POST:
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Report uploaded successfully!")
            return redirect('index')
    else:
        form = ReportForm()

    recent_searches = SearchHistory.objects.all()[:4]
    reports = ProjectReport.objects.all().order_by('-uploaded_at')
    
    view = request.GET.get('view', 'weather')

    context = {
        'weather': weather_data,
        'recent_searches': recent_searches,
        'reports': reports,
        'form': form,
        'view': view
    }
    return render(request, 'main/index.html', context)

def delete_report(request, report_id):
    try:
        report = ProjectReport.objects.get(id=report_id)
        # Delete the actual file from disk
        if report.report_file:
            report.report_file.delete()
        # Delete the database record
        report.delete()
        messages.success(request, "Report deleted successfully!")
    except ProjectReport.DoesNotExist:
        messages.error(request, "Report not found.")
    
    return redirect('/?view=reports')


