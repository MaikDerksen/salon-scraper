from city_salon_scraper import SalonScraper
from salon_scraper import SalonSearch
import os
import json

def main():
    city_input = input("Enter the city (e.g., Berlin): ")
    scraper = SalonScraper(format_name_city(city_input))
    scraper.scrape_salons()
    scraper.save_to_txt()
    
    # Use city_input instead of the input function for the filename
    with open(f"salon_names/{format_name_city(city_input)}_salons.txt", 'r', encoding='utf-8') as salon_file:
        for salon_name in salon_file:
            salon_search = SalonSearch(salon_name.strip())  # Strip newline characters
            soup = salon_search.fetch_salon_page()

            if soup:
                salon_search.extract_salon_details(soup)
                salon_details = salon_search.get_salon_details()
                
                # Create a folder for JSON files if it doesn't exist
                folder_path = 'json'
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Use the formatted salon name for the JSON filename
                filename = f"{salon_search.format_name()}_details.json"
                file_path = os.path.join(folder_path, filename)

                with open(file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(salon_details, json_file, ensure_ascii=False, indent=4)
                print(f"Data saved to {file_path}")

def format_name_city(name: str):
    return (name.lower()
        .replace(' ', '-').replace("'", "-").replace('"', "-")
        .replace("+", "-").replace("|", "-").replace(",", "-")
        .replace("ß", "ss").replace('ä', 'ae').replace('ö', 'oe')
        .replace('ü', 'ue').replace("@", "-").replace("(", "-")
        .replace(")", "-").replace(".", "-").replace("&", "-")
        .replace("/", "-").replace(":", "-").replace(";", "-")
        .replace("?", "-").replace("!", "-").replace("#", "-")
        .replace("=", "-").replace("%", "-").replace("‘", "-")
        .replace("•", "-").replace("*", "-").replace("…", "-")
        .replace("©", "-").replace("$", "-").replace("€", "-")
        .replace("<", "-").replace(">", "-").replace("[", "-")
        .replace("]", "-").replace("{", "-").replace("}", "-")
        .replace("^", "-").replace("~", "-").replace("`", "-")
        .replace("\\", "-").replace("°", "-").replace("™", "-")
        .replace("®", "-").replace("√", "-").replace("—", "-")
        .replace("---", "-").replace("--", "-")
        .strip('-'))

if __name__ == "__main__":
    main()
