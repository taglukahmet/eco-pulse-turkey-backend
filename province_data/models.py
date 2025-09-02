from django.db import models
import uuid
from django.db.models import JSONField

class City(models.Model):
    SENTIMENT_OPTIONS = [
        ('Çok Olumlu', 'Çok Olumlu'),
        ('Olumlu', 'Olumlu'),
        ('Nötr', 'Nötr'),
        ('Olumsuz', 'Olumsuz'),
        ('Çok Olumsuz', 'Çok Olumsuz')
    ]

    REGIONS = [
        ('İç Anadolu Bölgesi','İç Anadolu Bölgesi'),
        ('Doğu Anadolu Bölgesi','Doğu Anadolu Bölgesi'),
        ('Güneydoğu Anadolu Bölgesi','Güneydoğu Anadolu Bölgesi'),
        ('Ege Bölgesi', 'Ege Bölgesi'),
        ('Marmara Bölgesi','Marmara Bölgesi'),
        ('Akdeniz Bölgesi','Akdeniz Bölgesi'),
        ('Karadeniz Bölgesi','Karadeniz Bölgesi')
    ]
    NAMES = [
        ('X (Twitter)', 'X (Twitter)'),
        ('Next Sosyal', 'Next Sosyal'),
        ('Instagram', 'Instagram')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, null=False, choices=NAMES)
    mainHashtag = models.CharField(null=True, blank=True)
    sentiment = models.JSONField(default=dict, null=True, blank=True)
    inclination = models.CharField(default='', choices=SENTIMENT_OPTIONS)
    hashtags_list = models.JSONField(default=dict, null=False)
    topics_list = models.JSONField(default=dict, null=True, blank=True)
    region = models.CharField(null=False, choices=REGIONS)
    d = models.CharField(null=False)

    def set_sentiment(self, positive, neutral, negative):
        self.sentiment = {"Pozitif":positive, "Nötr":neutral, "Negatif":negative}
        self.save()

    def set_inclination(self):
        total = 0
        for val in self.sentiment.values():
            total += val
        pozitif = (float(int((self.sentiment["Pozitif"]/total)*10000)))/100
        notr = (float(int((self.sentiment["Nötr"]/total)*10000)))/100
        point = pozitif + notr/2
        if (point <= 100 and point >=80):
            self.inclination = 'Çok Olumlu'
        elif (point < 80 and point >= 60):
            self.inclination = 'Olumlu'
        elif (point < 60 and point >= 40):
            self.inclination = 'Nötr'
        elif (point < 40 and point >= 20):
            self.inclination = 'Olumsuz'
        elif (point <20 and point >= 0):
            self.inclination = 'Çok Olumsuz'
        self.save()

    def organize_hashtags(self):
        tags = {k: v for k, v in sorted(self.hashtags_list.items(), key=lambda item: item[1], reverse=True)}
        self.hashtags_list = tags
        for key in tags.keys():
            self.mainHashtag = key
            break
        self.save()

    def organize_topics(self):
        tops = {k: v for k, v in sorted(self.topics_list.items(), key=lambda item: item[1], reverse=True)}
        self.topics_list = tops
        self.save()

    def __str__(self):
        return self.name
    
class DataofPlatforms(models.Model):
    SENTIMENT_OPTIONS = [
        ('Çok Olumlu', 'Çok Olumlu'),
        ('Olumlu', 'Olumlu'),
        ('Nötr', 'Nötr'),
        ('Olumsuz', 'Olumsuz'),
        ('Çok Olumsuz', 'Çok Olumsuz')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, null=False)
    posts = models.PositiveBigIntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='platforms')
    mainTopic = models.CharField(null=False)
    mainHashtag = models.CharField(null=False)
    sentiment = models.JSONField(default=dict, null=False)
    inclination = models.CharField(default='', choices=SENTIMENT_OPTIONS)
    hashtags_list = models.JSONField(default=dict, null=False)
    topics_list = models.JSONField(default=dict, null=False)
    date = models.DateField(null=True, blank=True)

    def set_sentiment(self, positive, neutral, negative):
        self.sentiment = {"Pozitif":positive, "Nötr":neutral, "Negatif":negative}
        self.save()

    def set_inclination(self):
        total = 0
        for val in self.sentiment.values():
            total += val
        pozitif = (float(int((self.sentiment["Pozitif"]/total)*10000)))/100
        notr = (float(int((self.sentiment["Nötr"]/total)*10000)))/100
        point = pozitif + notr/2
        if (point <= 100 and point >=80):
            self.inclination = 'Çok Olumlu'
        elif (point < 80 and point >= 60):
            self.inclination = 'Olumlu'
        elif (point < 60 and point >= 40):
            self.inclination = 'Nötr'
        elif (point < 40 and point >= 20):
            self.inclination = 'Olumsuz'
        elif (point <20 and point >= 0):
            self.inclination = 'Çok Olumsuz'
        self.save()

    def organize_hashtags(self):
        tags = {k: v for k, v in sorted(self.hashtags_list.items(), key=lambda item: item[1], reverse=True)}
        self.hashtags_list = tags
        for key in tags.keys():
            self.mainHashtag = key
            break
        self.save()

    def organize_topics(self):
        tops = {k: v for k, v in sorted(self.topics_list.items(), key=lambda item: item[1], reverse=True)}
        self.topics_list = tops
        for key in tops.keys():
            self.mainTopic = key
            break
        self.save()

    def __str__(self):
        return self.name

class NationalDataLog(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True, blank=True)
    topics_list = models.JSONField(default=dict, null=False)
    posts = models.PositiveBigIntegerField()

    def set_posts(self):
        post = 0
        cities = City.objects.all()
        for city in cities:
            platforms = DataofPlatforms.objects.filter(city = city, date = self.date)
            for platform in platforms:
                post += platform.posts
        self.posts = post
        self.save()


    def organize_topics(self):
        tops = {k: v for k, v in sorted(self.topics.items(), key=lambda item: item[1], reverse=True)}
        self.hashtags = tops
        for key in tops.keys():
            self.mainTopic = key
            break
        self.save()

    def __str__(self):
        return f"{self.date} dated national data"





