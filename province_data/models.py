from django.db import models
import uuid
from django.db.models import JSONField
from django.db.models import Sum

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
    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, null=False)
    mainHashtag = models.CharField(null=True, blank=True)
    sentiment = models.JSONField(default=dict, null=True, blank=True)
    inclination = models.CharField(default='', choices=SENTIMENT_OPTIONS)
    hashtags_list = models.JSONField(default=dict, null=True, blank=True)
    topics_list = models.JSONField(default=dict, null=True, blank=True)
    region = models.CharField(null=False, choices=REGIONS)

    def set_sentiment(self, positive, neutral, negative):
        self.sentiment = {"Pozitif":positive, "Nötr":neutral, "Negatif":negative}
        self.save()

    def set_sentiment_with_social(self):
        positive = 0
        neutral = 0
        negative = 0
        for platform in self.platforms.all():
            positive += platform.sentiment["Pozitif"]
            neutral += platform.sentiment["Nötr"]
            negative += platform.sentiment["Negatif"]
        self.sentiment = {"Pozitif":positive, "Nötr":neutral, "Negatif":negative}
        self.save()

    def set_inclination(self):
        total = 0
        for val in self.sentiment.values():
            total += val
        if total != 0:
            pozitif = (float(int((self.sentiment["Pozitif"]/total)*10000)))/100
            notr = (float(int((self.sentiment["Nötr"]/total)*10000)))/100
        else:
            pozitif = 0
            notr = 0
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

    def set_hashtags_with_social(self):
        platforms = self.platforms.all()
        hashtags_list = {}
        for platform in platforms:
            hashlist = platform.hashtags_list

            if not isinstance(hashlist, dict):
                continue
            for key, val in hashlist.items():
                hashtags_list[key] = hashtags_list.get(key, 0) + val
    
        self.hashtags_list = hashtags_list
        self.save()

    def organize_topics(self):
        tops = {k: v for k, v in sorted(self.topics_list.items(), key=lambda item: item[1], reverse=True)}
        self.topics_list = tops
        self.save()

    def set_topics_with_social(self):
        platforms = self.platforms.all()
        topics_list = {}
        for platform in platforms:
            toplist = platform.topics_list
            if not isinstance(toplist, dict):
                continue
            for key, val in toplist.items():
                topics_list[key] = topics_list.get(key, 0) + val
        self.topics_list = topics_list
        self.save()

    def __str__(self):
        return self.name
    
class DataofPlatforms(models.Model):
    NAMES = [
        ('X (Twitter)', 'X (Twitter)'),
        ('NSosyal', 'NSosyal'),
        ('Instagram', 'Instagram')
    ]
    SENTIMENT_OPTIONS = [
        ('Çok Olumlu', 'Çok Olumlu'),
        ('Olumlu', 'Olumlu'),
        ('Nötr', 'Nötr'),
        ('Olumsuz', 'Olumsuz'),
        ('Çok Olumsuz', 'Çok Olumsuz')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, null=False, choices=NAMES)
    posts = models.PositiveBigIntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='platforms')
    mainTopic = models.CharField(null=True, blank=True)
    mainHashtag = models.CharField(null=True, blank=True)
    sentiment = models.JSONField(default=dict, null=True, blank=True)
    inclination = models.CharField(default='', choices=SENTIMENT_OPTIONS)
    hashtags_list = models.JSONField(default=dict, null=True, blank=True)
    topics_list = models.JSONField(default=dict, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def set_sentiment(self, positive, neutral, negative):
        self.sentiment = {"Pozitif":positive, "Nötr":neutral, "Negatif":negative}
        self.save()

    def set_inclination(self):
        total = 0
        for val in self.sentiment.values():
            total += val
        if total != 0:
            pozitif = (float(int((self.sentiment["Pozitif"]/total)*10000)))/100
            notr = (float(int((self.sentiment["Nötr"]/total)*10000)))/100
        else:
            pozitif = 0
            notr = 0
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
    topics_list = models.JSONField(default=dict, null=True, blank=True)
    posts = models.PositiveBigIntegerField(default=0)



    def set_posts(self):

        platforms_for_date = DataofPlatforms.objects.filter(date=self.date)
        aggregation_result = platforms_for_date.aggregate(total_posts=Sum('posts'))
        total_posts = aggregation_result.get('total_posts') or 0
    
        self.posts = total_posts
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





