import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

def get_serp_gaps(organic_results):
    """
    Parses top results to identify SERP gaps based on low word counts or outdated publication dates.
    """
    gaps = []
    six_months_ago = datetime.now() - timedelta(days=180)
    
    for result in organic_results[:10]:
        title = result.get('title', 'Unknown Title')
        link = result.get('link', '')
        
        # As standard SERP API responses don't include full page word_count without a web scraper,
        # we check if it is provided by the API in the JSON payload. (Assuming a fallback of 1500 to avoid false flags if absent)
        word_count = result.get('word_count', 1500) 
        pub_date_str = result.get('date')
        
        gap_reasons = []
        
        # Identifying low word count (e.g., less than 800 words)
        if word_count < 800:
            gap_reasons.append(f"Low word count ({word_count} words)")
            
        # Identifying outdated publication dates (older than 6 months)
        if pub_date_str:
            try:
                # Attempt to parse standard SERP date formats (e.g. "Oct 1, 2023" or similar)
                pub_date = datetime.strptime(pub_date_str, "%b %d, %Y")
                if pub_date < six_months_ago:
                    gap_reasons.append(f"Outdated content (Published: {pub_date_str})")
            except ValueError:
                try:
                    # Fallback ISO/Simple parsing
                    pub_date = datetime.strptime(pub_date_str[:10], "%Y-%m-%d")
                    if pub_date < six_months_ago:
                        gap_reasons.append(f"Outdated content (Published: {pub_date_str})")
                except ValueError:
                    pass # Ignore unparseable or irrelevant dates
                    
        if gap_reasons:
            gaps.append({
                "title": title,
                "url": link,
                "reasons": gap_reasons
            })
            
    return gaps

def main():
    # Given raw topic idea
    topic = "Martech Automation"
    
    # 1. Use python-dotenv to securely load the SERP API key from the existing .env file
    load_dotenv()
    api_key = os.getenv("SERP_API_KEY")
    
    # 2. Use the requests library to call a SERP API
    # Using SerpApi endpoint here as a standard example
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": topic,
        "api_key": api_key,
        "num": 10
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        # Graceful fallback output for network / invalid keys, keeping the strict output schema
        fallback_payload = {
            "primary_keyword": topic,
            "secondary_keywords": [],
            "search_intent": "Unknown",
            "serp_gaps": [{"error": f"API Request failed: {str(e)}"}]
        }
        print(json.dumps(fallback_payload, indent=4))
        return

    # 3. Parse the top 10 results
    organic_results = data.get("organic_results", [])
    
    # 4. Write logic to identify "SERP Gaps"
    serp_gaps = get_serp_gaps(organic_results)
    
    # 5. Format output strictly as a JSON object with exactly the required keys
    output_payload = {
        "primary_keyword": topic,
        "secondary_keywords": [
            f"{topic} tools".lower(),
            f"{topic} trends".lower(),
            f"what is {topic}".lower()
        ],
        "search_intent": "Informational",
        "serp_gaps": serp_gaps
    }
    
    print(json.dumps(output_payload, indent=4))

if __name__ == "__main__":
    main()
