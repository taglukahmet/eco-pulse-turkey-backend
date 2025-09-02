from .models import *
from django.utils import timezone
from datetime import timedelta

def prepare_city(city_id):
    this_city = City.objects.get(id= city_id)
    this_city.set_inclination()
    this_city.organize_hashtags()
    if this_city.topics_list:
        this_city.organize_topics()
    this_city.save()
    return this_city

def create_global_hashtags(cities):
    hashtags_list = {}
    for city in cities:
        for key, val in city.hashtags_list.items():
            if key in hashtags_list.keys():
                itemval = hashtags_list[key]
                hashtags_list.update({key:itemval + val})
            else: 
                hashtags_list.update({key:val})
    hashtags_list = {k: v for k, v in sorted(hashtags_list.items(), key=lambda item: item[1], reverse=True)}
    hashtags_list = list (hashtags_list.keys())
    return hashtags_list

def generate_global_sentiment(cities):
    sentiment={"positive":0 , "neutral":0 , "negative":0}
    for city in cities:
        p = sentiment["positive"]
        sentiment.update({"positive":city.sentiment["Pozitif"] + p})
        n = sentiment["neutral"]
        sentiment.update({"neutral":city.sentiment["Nötr"] + n})
        e = sentiment["negative"]
        sentiment.update({"negative":city.sentiment["Negatif"] + e})

    p = sentiment["positive"]
    n = sentiment["neutral"]
    e = sentiment["negative"]
    c = p+n+e
    sentiment.update({"positive":(float(int((p/c)*100000)))/1000})
    sentiment.update({"neutral": (float(int((n/c)*100000)))/1000})
    sentiment.update({"negative": (float(int((e/c)*100000)))/1000})
    return sentiment

def create_global_topics(cities):
    topics_list = {}
    for city in cities:
        for key, val in city.topics_list.items():
            if key in topics_list.keys():
                itemval = topics_list[key]
                topics_list.update({key:itemval + val})
            else: 
                topics_list.update({key:val})
    topics_list = {k: v for k, v in sorted(topics_list.items(), key=lambda item: item[1], reverse=True)}
    topics = []
    for key, val in topics_list.items():
        topics.append({"name":key, "mentions":val, "trend":0})
    return topics

def generate_city_weekly_trends(city_id):
    trend = []
    city = City.objects.get(id = city_id)
    today = timezone.localdate()
    for i in range(0,6):
        day = today - timedelta(days=i)
        platforms = DataofPlatforms.objects.filter(city = city, date=day)
        posts = 0
        for platform in platforms:
            posts += platform.posts
        day_num = day.strftime('%w')
        day_name = ""
        match int(day_num):
            case 0:
                day_name = "Paz"
            case 1:
                day_name = "Pzt"
            case 2:
                day_name = "Sal"
            case 3:
                day_name = "Çar"
            case 4:
                day_name = "Per"
            case 5:
                day_name = "Cum"
            case 6:
                day_name = "Cmt"
        trend.insert(0,{"day":day_name, "volume":posts})
    return trend

def generate_national_weekly_trends():
    trend = []
    today = timezone.localdate()
    for i in range(0,6):
        day = today - timedelta(days=i)
        day_num = day.strftime('%w')
        day_name = ""
        match int(day_num):
            case 0:
                day_name = "Paz"
            case 1:
                day_name = "Pzt"
            case 2:
                day_name = "Sal"
            case 3:
                day_name = "Çar"
            case 4:
                day_name = "Per"
            case 5:
                day_name = "Cum"
            case 6:
                day_name = "Cmt"
        try:
            data = NationalDataLog.objects.get(date = day)
            data.set_posts()
            posts = data.posts
        except NationalDataLog.DoesNotExist:
            posts=0
        trend.insert(0,{"day":day_name, "volume":posts})
    return trend

def generate_regional_performance():
    REGIONS = [
        "İç Anadolu Bölgesi",
        "Doğu Anadolu Bölgesi",
        "Güneydoğu Anadolu Bölgesi",
        "Ege Bölgesi",
        "Marmara Bölgesi",
        "Akdeniz Bölgesi",
        "Karadeniz Bölgesi"
    ]
    performance = []
    today = timezone.localdate()
    yesterday = today - timedelta(days=1)
    cities = City.objects.all()
    for region in REGIONS:
        post = 0
        old_post = 0
        for city in cities:
            if city.region == region:
                platforms = DataofPlatforms.objects.filter(city=city, date=today)
                for platform in platforms:
                    post += platform.posts
        for city in cities:
            if city.region == region:
                platforms = DataofPlatforms.objects.filter(city=city, date=yesterday)
                for platform in platforms:
                    old_post += platform.posts
        if old_post != 0:
            margin = (((post/old_post)*100)-100)
        else: margin = 0
        margin = (float(int(margin*100)))/100
        marg = ""
        if margin > 0 :
            marg = "+"+str(margin)
        else:
            marg = str(margin) 
        
        performance.append({"region":region, "percentage":post, "trend":marg})
    post_total = 0
    for i in performance:
        for key in i.keys():
            if key == "percentage":
                post_total += i["percentage"]
    for i in performance:
        if post_total != 0:
            i.update({"percentage":(i["percentage"]/post_total)*100})
        else: i.update({"percentage": 0})
    return performance
                        
def generate_national_social():
    social = []
    PLATFORMS = {"X (Twitter)":"twitter", "Instagram":"instagram", "Next Sosyal":"next"}
    for platform in PLATFORMS.keys():
        detail = {"platform":platform, "icon":PLATFORMS[platform]}
        total_post = 0
        total_positive = 0
        total_total = 0
        platforms = DataofPlatforms.objects.filter(name = platform)
        for pltfrm in platforms:
            total_post += pltfrm.posts
            total_positive += pltfrm.sentiment["Pozitif"]
            total_total += pltfrm.sentiment["Pozitif"] + pltfrm.sentiment["Nötr"] + pltfrm.sentiment["Negatif"]
        avg_positive = 0
        if total_total != 0:
            avg_positive = (float(int((total_positive/total_total)*10000)))/100
        else: avg_positive = 0
        detail.update({"avgSentiment":avg_positive})
        detail.update({"totalPosts":total_post})
        cities = City.objects.all()
        for city in cities:
            max_city = {"": 0}
            post_city = 0
            pltfrms = city.platforms.filter(name = platform)
            for pltfrm in pltfrms:
                post_city += pltfrm.posts
            for key, val in max_city.items():
                if key == "" or post_city >= val:
                    max_city = {city.name : post_city}
        for key in max_city.keys():
            detail.update({"topRegion":key})
        hashtags_list = {}
        for pltfrm in platforms:
            for key, val in platform.hashtags_list.items():
                if key in hashtags_list.keys():
                    itemval = hashtags_list[key]
                    hashtags_list.update({key:itemval + val})
            else: 
                hashtags_list.update({key:val})
        hashtags_list = {k: v for k, v in sorted(hashtags_list.items(), key=lambda item: item[1], reverse=True)}
        mainHashtag = ""
        for key in hashtags_list.keys():
            mainHashtag = key
            break
        detail.update({"mainHashtag":mainHashtag})
        social.append(detail)
    return social

def generate_weekly_social():
    PLATFORMS = {"X (Twitter)":"twitter", "Instagram":"instagram", "Next Sosyal":"next"}
    social = []
    today = timezone.localdate()
    for i in range(0,6):
        day = today - timedelta(days=i)
        day_num = day.strftime('%w')
        day_name = ""
        match int(day_num):
            case 0:
                day_name = "Paz"
            case 1:
                day_name = "Pzt"
            case 2:
                day_name = "Sal"
            case 3:
                day_name = "Çar"
            case 4:
                day_name = "Per"
            case 5:
                day_name = "Cum"
            case 6:
                day_name = "Cmt"
        day_social = {"day":day_name}
        for platform in PLATFORMS.keys():
            total_platform = 0
            platforms = DataofPlatforms.objects.filter(name = platform, date = day)
            for pltfrm in platforms:
                total_platform += pltfrm.posts
            day_social.update({PLATFORMS[platform]:total_platform})
        social.insert(0, day_social)
    return social

def generate_city_social(city_id):
    city = City.objects.get(id = city_id)
    social = []
    PLATFORMS = {"X (Twitter)":"twitter", "Instagram":"instagram", "Next Sosyal":"next"}
    for platform in PLATFORMS.keys():
        detail = {"platform":platform, "icon":PLATFORMS[platform]}
        total_post = 0
        total_positive = 0
        total_neutral = 0
        total_negative = 0
        platforms = DataofPlatforms.objects.filter(name = platform, city = city)
        for pltfrm in platforms:
            total_post += pltfrm.posts
            total_positive += pltfrm.sentiment["Pozitif"]
            total_neutral += pltfrm.sentiment["Nötr"]
            total_negative += pltfrm.sentiment["Negatif"]
        total_total = total_neutral + total_negative + total_positive
        avg_positive = 0
        avg_neutral = 0
        avg_negative = 0
        if total_total != 0:
            avg_positive = (float(int((total_positive/total_total)*10000)))/100
            avg_neutral = (float(int((total_neutral/total_total)*10000)))/100
            avg_negative = (float(int((total_negative/total_total)*10000)))/100
        else:
            avg_negative = 0
            avg_neutral = 0
            avg_positive = 0
        sentiment = {"positive":avg_positive, "neutral":avg_neutral, "negative":avg_negative}
        detail.update({"sentiment":sentiment})
        detail.update({"posts":total_post})
        hashtags_list = {}
        for pltfrm in platforms:
            for key, val in platform.hashtags_list.items():
                if key in hashtags_list.keys():
                    itemval = hashtags_list[key]
                    hashtags_list.update({key:itemval + val})
            else: 
                hashtags_list.update({key:val})
        hashtags_list = {k: v for k, v in sorted(hashtags_list.items(), key=lambda item: item[1], reverse=True)}
        mainHashtag = ""
        for key in hashtags_list.keys():
            mainHashtag = key
            break
        detail.update({"mainHashtag":mainHashtag})
        topics_list = {}
        for pltfrm in platforms:
            for key, val in platform.topics_list.items():
                if key in topics_list.keys():
                    itemval = topics_list[key]
                    topics_list.update({key:itemval + val})
            else: 
                topics_list.update({key:val})
        topics_list = {k: v for k, v in sorted(topics_list.items(), key=lambda item: item[1], reverse=True)}
        maintopic = ""
        for key in topics_list.keys():
            maintopic = key
            break
        detail.update({"topTopic":maintopic})
        social.append(detail)
    for i in social:
        total_posts = 0
        for key, val in i.items():
            if key == "posts":
                total_posts += val
    for i in social:
        if total_posts != 0:
            impact = (float(int((i["posts"]/total_posts)*100)))/100
        else: impact = 0
        i.update({"impact":impact})
    return social
            
            

        
        
        





                

        
        


