# Salon Scraper

A Python application that scrapes salon information from the Treatwell website based on the salon name. The application retrieves details such as address, rating, and available services, then saves this information in a structured JSON format.

## Features

- Search for salons by name
- Scrape salon details including:
  - Name
  - Address
  - Rating and review count
  - List of services with prices, durations, and discounts
- Save the scraped data to a JSON file

## Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:MaikDerksen/salon-scraper.git

2. **Install Dependencies**
    ```bash
    pip install requests beautifulsoup4 os
    ```

## Usage

### To run the application, execute the following command in your terminal or command prompt:
```bash
python src/run_salon_search.py #Single Salon
or
python src/run_city_salon_search.py #All Salon in the City
```

### Enter in Terminal Salon to Scrape:
```bash
Enter the salon name:
```

### Example
```
Deinhard Friseurteam Rudow
```

### Console Output
```
Enter the salon name: Deinhard Friseurteam Rudow
Request successful for salon: Deinhard Friseurteam Rudow
Data saved to deinhard-friseurteam-rudow_details.json
```

### The Json File should look like this:
```json
{
    "name": "Deinhard Friseurteam Rudow",
    "address": "Neuköllner Str. 211, 12357 Berlin, Deutschland",
    "rating": "4,7",
    "rating_count": "177 Bewertungen",
    "services": [
        {
            "title": "Herren - Waschen, Schneiden & Föhnen",
            "price": "22 €",
            "strike": "N/A",
            "duration": "45 Min.",
            "discount": "No discount"
        },
        ...
    ]
}
```

## Contributing
Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue.