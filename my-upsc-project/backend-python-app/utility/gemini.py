from utility.config import get_gemini_api_key
import requests,json

GEMINI_API_KEY = get_gemini_api_key()

def call_gemini_api(prompt_messages):
    """
    Makes a synchronous API call to the Gemini API using the requests library.
    This function is called by the FastAPI endpoint.
    """
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API Key is not configured on the backend server.")

    payload = {
        "contents": prompt_messages,
        "generationConfig": {
            "responseMimeType": "text/plain"
        }
    }
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    try:
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, json=payload)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()

        if result.get('candidates') and result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts'):
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"LLM response structure unexpected: {json.dumps(result, indent=2)}")
            raise Exception("LLM did not return a valid response or content.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response from API: {e}")
        print(f"API Response Text: {response.text}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
