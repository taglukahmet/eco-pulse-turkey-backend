import json
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

def generate_json_file(output_filename="data_province.json"):
    """
    Creates a sample Python dictionary, then writes it to a JSON file.
    This function demonstrates the core logic of JSON file creation in Python.
    """
    try:
        # --- 1. Define the Data in a Python Dictionary ---
        # In your Django application, this dictionary would be built dynamically
        # with data you retrieve from your models.
        print("preparing data")
        output_data = []
        cities = City.objects.all()
        for city in cities:
            data = {
                "name":city.name,
                "region":city.region
            }
            output_data.append(data)
        print("Data structure created.")

        # --- 2. Write the Data to a JSON file ---
        # The 'with open(...)' syntax ensures the file is properly closed,
        # even if errors occur.
        print(f"Writing data to '{output_filename}'...")
        with open(output_filename, 'w', encoding='utf-8') as json_file:
            # json.dump() serializes the Python dictionary into a JSON formatted string
            # and writes it to the file.
            # - `output_data`: The Python object to write.
            # - `json_file`: The file object to write to.
            # - `indent=4`: This makes the JSON file human-readable with pretty-printing.
            # - `ensure_ascii=False`: Allows non-ASCII characters (like accents) to be written as-is.
            json.dump(output_data, json_file, indent=4, ensure_ascii=False)

        print(f"\nSuccessfully created '{output_filename}' with the sample data.")

    except IOError as e:
        print(f"Error writing to file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # This block will only run when the script is executed directly.
    # It calls the function to generate the JSON file.
    generate_json_file()

