from django.db import models

class SearchHistory(models.Model):
    city_name = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=20, default='01d')
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']

    def __str__(self):
        return f"{self.city_name} at {self.searched_at}"

class ProjectReport(models.Model):
    title = models.CharField(max_length=200)
    report_file = models.FileField(upload_to='reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
