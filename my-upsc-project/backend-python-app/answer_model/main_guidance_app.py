# answer_model/main_guidance_app.py

import json
import requests # Import the requests library
import asyncio # Keep asyncio for the main loop, though call_llm_api is synchronous
# Import the evaluation matrix components
# CORRECTED IMPORT: Assuming evaluation_matrix.py is in the same directory
from evaluation_matrix import (
    get_evaluation_criteria,
    INTRODUCTION_COMPETENCE,
    CONCLUSION_COMPETENCE,
    BODY_COMPETENCE,
)

# Function to call LLM API using requests (synchronous for local execution)
def call_llm_api(prompt_messages):
    """ 
    Makes a synchronous API call to the Gemini API using the requests library.
    This is suitable for local Python execution (e.g., in VS Code).

    Args:
        prompt_messages (list): A list of dictionaries representing the chat history
                                (role and parts).

    Returns:
        str: The generated text response from the LLM.
    """
    # IMPORTANT: Replace "YOUR_GEMINI_API_KEY" with your actual Google Cloud API Key.
    # You can get one from the Google Cloud Console or Google AI Studio.
    # This key is necessary for local execution.
    api_key = "AIzaSyBOSNdJ-e7EJA0C3Fmjv7_Of3MDGOdXZeE" # <--- REPLACE THIS WITH YOUR ACTUAL API KEY ---

    if api_key == "YOUR_GEMINI_API_KEY" or not api_key:
        raise ValueError("Please replace 'YOUR_GEMINI_API_KEY' with your actual API key to run locally.")

    payload = {
        "contents": prompt_messages,
        "generationConfig": {
            "responseMimeType": "text/plain" # We expect structured text guidance
        }
    }
    # Using gemini-2.0-flash as specified in the instructions
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    print("\n--- Sending request to LLM ---")
    print(f"Prompt sent: {json.dumps(prompt_messages, indent=2)}")

    try:
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, json=payload)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()

        if result.get('candidates') and result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts'):
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            # Handle cases where the response structure is unexpected or content is missing
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


async def generate_upsc_guidance(question: str, word_limit: int = 150):
    """
    Generates structured guidance for a UPSC Mains answer based on the
    provided question and the defined evaluation matrix.

    Args:
        question (str): The UPSC Mains question text.
        word_limit (int): The expected word limit for the answer (150 or 250).

    Returns:
        str: Structured guidance from the LLM.
    """

    # Dynamically get word limit details for Intro/Conclusion
    intro_wl_info = INTRODUCTION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]
    concl_wl_info = CONCLUSION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]

    # Construct the system message using the evaluation matrix
    # This guides the LLM on its persona and the rules it must follow.
    system_prompt = f"""
    You are an expert UPSC Mains examiner from Ajayvision. Your task is to provide comprehensive,
    structured, and actionable guidance on how a student should write a high-quality answer for a
    given UPSC Mains question.

    Strictly adhere to the following evaluation criteria and guidelines:

    **I. Overall Answer Competence (General Principles):**
    - Wholesome Nature: {get_evaluation_criteria('overall_answer_competence')['wholesome_nature']}
    - Clarity & Cohesion: {get_evaluation_criteria('overall_answer_competence')['clarity_cohesion']}
    - Adherence to Demand: {get_evaluation_criteria('overall_answer_competence')['adherence_to_demand']}
    - Examiner Perception: {get_evaluation_criteria('overall_answer_competence')['examiner_perception']}
    - Word Limit Adherence: {get_evaluation_criteria('overall_answer_competence')['word_limit_adherence']}

    **II. Introduction Competence:**
    - Aim & Purpose: {json.dumps(INTRODUCTION_COMPETENCE['aim_purpose'])}
    - Content Requirements: {json.dumps(INTRODUCTION_COMPETENCE['content_requirements'])}
    - Word Limit for {word_limit} words: {intro_wl_info['words']} (approx. {intro_wl_info['time_minutes']} minute)
    - Types of Introduction & Utilization: {json.dumps(INTRODUCTION_COMPETENCE['types'], indent=2)}
        - Note: Choose the most suitable type based on the question's nature.

    **III. Body Competence (General Guidelines):**
    - Content Depth & Relevance: {BODY_COMPETENCE['content_depth_relevance']}
    - Multi-dimensionality: {BODY_COMPETENCE['multi_dimensionality']}
    - Evidence & Examples: {BODY_COMPETENCE['evidence_examples']}
    - Logical Flow: {BODY_COMPETENCE['logical_flow']}
    - Subheadings & Bullet Points: {BODY_COMPETENCE['subheadings_bullet_points']}

    **IV. Conclusion Competence:**
    - Aim & Purpose: {json.dumps(CONCLUSION_COMPETENCE['aim_purpose'])}
    - Word Limit for {word_limit} words: {concl_wl_info['words']} (approx. {concl_wl_info['time_minutes']} minute)
    - Types of Conclusion & Utilization: {json.dumps(CONCLUSION_COMPETENCE['types'], indent=2)}
        - Note: Choose the most suitable type based on the discussion in the body and question's directive.
    - Distinction from Way Forward: {json.dumps(CONCLUSION_COMPETENCE['distinction_from_way_forward'])}

    Your output should be structured as follows:
    ## UPSC Mains Answer Guidance
    ### 1. Question Deconstruction
    * **Directive Word(s):** [Identify]
    * **Keywords:** [Identify]
    * **Core Demand:** [Summarize what the question asks]

    ### 2. Introduction Strategy
    * **Recommended Type(s):** [Suggest 1-2 types from the matrix with justification]
    * **Reasoning:** [Explain why this type is suitable for the given question]
    * **Example Opening Hook (Approx. {intro_wl_info['words']}):** "[Provide a concise example]"

    ### 3. Body - Key Dimensions/Points to Cover
    * [Use bullet points or subheadings to list 3-5 main aspects/arguments relevant to the question. For each, suggest brief content and potential examples/data/facts.]
    * **A. [Dimension/Point 1]:** [Brief explanation, suggested content, e.g., facts/examples]
    * **B. [Dimension/Point 2]:** [Brief explanation, suggested content, e.g., facts/examples]
    * ... (add more points as relevant)

    ### 4. Conclusion Strategy
    * **Recommended Type(s):** [Suggest 1-2 types from the matrix with justification]
    * **Reasoning:** [Explain why this type is suitable]
    * **Example Closing Statement (Approx. {concl_wl_info['words']}):** "[Provide a concise example]"

    ### 5. Value Addition Points
    * [Suggest specific additional points like relevant articles, reports, committees, data, recent events, key terms that can enhance the answer.]

    ### 6. Common Pitfalls to Avoid
    * [List 3-5 common mistakes relevant to the question or general UPSC answer writing that students should avoid.]

    ### 7. Word Limit Suggestion
    * For a {word_limit}-word answer:
        * Introduction: {intro_wl_info['words']}
        * Body: ~{word_limit - (int(intro_wl_info['words'].split('-')[0]) + int(concl_wl_info['words'].split('-')[0]))} words (approximate)
        * Conclusion: {concl_wl_info['words']}
    """

    # Construct the user message (the actual question)
    user_message = f"Please provide structured answer writing guidance for the following UPSC Mains question (word limit: {word_limit} words):\n\nQuestion: {question}"

    chat_history = [
        {"role": "user", "parts": [{"text": system_prompt}]},
        {"role": "user", "parts": [{"text": user_message}]}
    ]

    print("\nGenerating guidance, please wait...")
    # Directly call the synchronous function
    guidance = call_llm_api(chat_history)
    return guidance

async def main():
    """
    Main function to run the UPSC answer guidance application.
    """
    print("Welcome to Ajayvision UPSC Answer Writing Guidance System!")
    print("This tool will help you structure your Mains answers effectively.")

    while True:
        user_question = input("\nEnter the UPSC Mains question (type 'quit' to exit): \n")
        if user_question.lower() == 'quit':
            break

        try:
            word_limit_input = input("Enter the word limit for this question (150 or 250): ")
            word_limit = int(word_limit_input)
            if word_limit not in [150, 250]:
                print("Invalid word limit. Please enter either 150 or 250.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number for the word limit.")
            continue

        # Await the async function that now internally calls the synchronous API function
        guidance = await generate_upsc_guidance(user_question, word_limit)
        print(guidance)

    print("\nThank you for using Ajayvision Guidance System. Happy learning!")

# To run the asynchronous main function
if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting the application.")
    except ValueError as ve: # Catch the API key error
        print(f"Configuration Error: {ve}")
    except Exception as e: # Catch other potential errors
        print(f"An unexpected error occurred: {e}")

