from salon_scraper import SalonSearch
import json
import os

# Main Program
if __name__ == "__main__":
    salon_name = input("Enter the salon name: ")
    salon_search = SalonSearch(salon_name)
    soup = salon_search.fetch_salon_page()

    if soup:
        salon_search.extract_salon_details(soup)
        salon_details = salon_search.get_salon_details()
        
        folder_path = 'json'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        filename = f"{salon_search.format_name()}_details.json"
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(salon_details, json_file, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}")

        #print(salon_details)
