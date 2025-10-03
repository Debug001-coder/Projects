#             python Linkedinsearches.py  

import webbrowser
import time
import requests
from serpapi import GoogleSearch

# Retry logic for API calls
def search_with_retry(params, max_retries=3):
    for attempt in range(max_retries):
        try:
            search = GoogleSearch(params)
            return search.get_dict()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}. Retrying ({attempt + 1}/{max_retries})...")
            time.sleep(2)
    return {}

# Open profiles with delay
def open_profiles(profiles, delay=7):
    for link in profiles:
        print(f"Opening: {link}")
        webbrowser.open(link)
        time.sleep(delay)

# Perform LinkedIn profile search
def google_search(query, countries, schools, companies, start, end, num_results):
    api_key = "Your SerpAPI Key"  # <-- Replace with your SerpAPI Key
    search_results = []

    for country in countries:
        search_query = f'{query} site:linkedin.com/in/'

        if country.lower() != "any":
            search_query += f' "{country}"'

        if schools[0].lower() != "any":
            school_filter = " OR ".join([f'"{school.strip()}"' for school in schools])
            search_query += f' ({school_filter})'

        if companies[0].lower() != "any":
            company_filter = " OR ".join([f'"{company.strip()}"' for company in companies])
            search_query += f' ({company_filter})'

        params = {
            "engine": "google",
            "q": search_query,
            "num": num_results,
            "api_key": api_key
        }

        results = search_with_retry(params)

        links = [res["link"] for res in results.get("organic_results", []) if "linkedin.com/in/" in res["link"]]
        search_results.extend(links)

    unique_profiles = list(dict.fromkeys(search_results))
    return unique_profiles[start - 1:end]

# MAIN
if __name__ == "__main__":
    query = input("Enter search query (e.g., Data Scientist): ").strip()
    countries = [c.strip() for c in input("Enter country names (comma-separated, 'any' for all): ").split(",")]

    # School handling
    schools = []
    if any(c.lower() == "india" for c in countries):
        block = input("India selected. Enter institute block (IIT, NIT, IIIT, DTU, NSUT or 'any'): ").strip().lower()

        indian_universities = {
            "iit": ["IIT Delhi", "IIT Bombay", "IIT Madras", "IIT Kharagpur"],
            "nit": ["NIT Trichy", "NIT Surathkal", "NIT Warangal"],
            "iiit": ["IIIT Hyderabad", "IIIT Delhi", "IIIT Allahabad"],
            "dtu": ["DTU"],
            "nsut": ["NSUT"]
        }

        if block != "any" and block in indian_universities:
            schools = indian_universities[block]
        else:
            schools = sum(indian_universities.values(), [])
    else:
        schools_input = input("Enter school names (comma-separated, or 'any'): ").strip()
        schools = [s.strip() for s in schools_input.split(",")] if schools_input.lower() != "any" else ["any"]

    # Company handling
    companies_input = input("Enter company names (comma-separated, or 'any'): ").strip()
    companies = [c.strip() for c in companies_input.split(",")] if companies_input.lower() != "any" else ["any"]

    # Fallback defaults
    if not schools:
        schools = ["any"]
    if not companies:
        companies = ["any"]

    start = int(input("Enter profile start number: "))
    end = int(input("Enter profile end number: "))
    num_results = int(input("Enter the number of profiles to load from Google: "))

    profiles = google_search(query, countries, schools, companies, start, end, num_results)

    if profiles:
        print(f"\nFound {len(profiles)} profiles:")
        for idx, profile in enumerate(profiles, start=1):
            print(f"{idx}. {profile}")

        choice = input("\nDo you want to open these profiles? (yes/no): ").strip().lower()
        if choice == "yes":
            open_profiles(profiles, delay=7)
        else:
            print("Profiles not opened.")
    else:
        print("No profiles found. Try different filters or check your API key.")
