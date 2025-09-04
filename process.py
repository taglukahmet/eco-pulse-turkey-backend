import os
import django
import json

# --- Django Setup Boilerplate (MUST BE AT THE TOP) ---
print("Setting up Django environment...")
# Replace 'eco_pulse_turkey_backend' if your project folder name is different
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eco_pulse_turkey_backend.settings')
django.setup()
print("Django environment is ready.")
# --- End of Setup ---


# ✅ Now it is safe to import your Django models
from province_data.models import City, DataofPlatforms, NationalDataLog


def main():
    """
    Your main script logic goes here.
    """
    # Assuming 'settings.BASE_DIR' is what you intended for the project root
    from django.conf import settings
    file_path = settings.BASE_DIR / 'ozet6.json'

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for platform in data:
        try:
            # Assuming platform['city'] is the name of the city
            city = City.objects.get(name=platform['city'].capitalize())
            pltfrm = DataofPlatforms.objects.create(
                name=platform['name'].capitalize(), 
                city=city, 
                posts=platform['posts'], 
                hashtags_list=platform['hashtags_list'], 
                topics_list=platform['topics_list'], 
                date=platform['date']
            )
            
            # Using .get() is safer than direct access, prevents KeyErrors
            positive = platform.get('sentiment', {}).get('Pozitif', 0)
            neutral = platform.get('sentiment', {}).get('Nötr', 0)
            negative = platform.get('sentiment', {}).get('Negatif', 0)
            
            pltfrm.set_sentiment(positive, neutral, negative)
            pltfrm.set_inclination()
            pltfrm.organize_hashtags()
            pltfrm.organize_topics()

        except City.DoesNotExist:
            print(f"WARNING: City '{platform['city']}' not found in the database. Skipping.")
        except Exception as e:
            print(f"An error occurred while processing platform {platform.get('name')}: {e}")

    print("\nResetting and recalculating city-wide data...")
    print(f"Processing {len(data)} platforms from JSON file...")
    
    for city in City.objects.all():
        city.hashtags_list = {}
        city.topics_list = {}
        city.set_sentiment(0, 0, 0)
        city.set_sentiment_with_social()
        city.set_inclination()
        city.set_hashtags_with_social()
        city.set_topics_with_social()
        city.organize_hashtags()
        city.organize_topics()

    print("\nUpdating national data logs...")
    for platform in DataofPlatforms.objects.all():
        try:
            # Using get_or_create is cleaner and safer
            log, created = NationalDataLog.objects.get_or_create(date=platform.date)
            log.set_posts()
        except Exception as e:
            print(f"An error occurred while updating national log for date {platform.date}: {e}")
            
    print("\nScript finished successfully!")


if __name__ == "__main__":
    main()