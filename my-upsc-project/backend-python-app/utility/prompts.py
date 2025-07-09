from utility.UPSC_evaluation_matrix import (
    get_evaluation_criteria,
    INTRODUCTION_COMPETENCE,
    CONCLUSION_COMPETENCE,
    BODY_COMPETENCE,
)
from utility.gemini import call_gemini_api
import json
from utility.logger import logger

def generate_upsc_guidance_logic(question: str, word_limit: int = 150):
    """
    Generates the system prompt using the evaluation matrix and calls the LLM.
    This logic is directly adapted from your main_guidance_app.py.
    """
    intro_wl_info = INTRODUCTION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]
    concl_wl_info = CONCLUSION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]

    system_prompt = f"""
    You are an expert UPSC Civil Services (Main) examiner from VisionIAS. Your task is to provide comprehensive,
    structured, and actionable guidance on how a student should write a high-quality answer for a
    given UPSC Civil Services (Main) question.

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

    Your output must strictly follow this structure using '###' for each main section heading.
    ## UPSC Civil Services (Main) Answer Guidance
    ### 1. Question Deconstruction
    Directive Word(s): **[Identify]**\nKeywords: **[Identify]**\nCore Demand: [Summarize what the question asks]

    ### 2. Introduction Strategy
    Recommended Type(s): [Suggest 1-2 types from the matrix with justification]
    Reasoning: [Explain why this type is suitable for the given question]
    Example Opening Hook (Approx. {intro_wl_info['words']}): "[Provide a concise example]"

    ### 3. Body - Key Dimensions/Points to Cover
    [Use bullet points or subheadings to list 3-5 main aspects/arguments relevant to the question. For each, suggest brief content and potential examples/data/facts.]
    A. [Dimension/Point 1]: [Brief explanation, suggested content, e.g., facts/examples]
    B. [Dimension/Point 2]: [Brief explanation, suggested content, e.g., facts/examples]
    ... (add more points as relevant)

    ### 4. Conclusion Strategy
    Recommended Type(s): [Suggest 1-2 types from the matrix with justification]
    Reasoning: [Explain why this type is suitable]
    Example Closing Statement (Approx. {concl_wl_info['words']}): "[Provide a concise example]"

    ### 5. Value Addition Points
    [Suggest specific additional points like relevant articles, reports, committees, data, recent events, key terms that can enhance the answer.]

    ### 6. Common Pitfalls to Avoid
    [List 3-5 common mistakes relevant to the question or general UPSC Civil Services (Main) answer writing that students should avoid.]

    ### 7. Word Limit Suggestion
    For a {word_limit}-word answer:
        Introduction: {intro_wl_info['words']}
        Body: ~{word_limit - (int(intro_wl_info['words'].split('-')[0]) + int(concl_wl_info['words'].split('-')[0]))} words (approximate)
        Conclusion: {concl_wl_info['words']}
    """

    user_message = f"Please provide structured answer writing guidance for the following UPSC Civil Services (Main) question (word limit: {word_limit} words):\n\nQuestion: {question}"

    chat_history = [
        {"role": "user", "parts": [{"text": system_prompt}]},
        {"role": "user", "parts": [{"text": user_message}]}
    ]

    return call_gemini_api(chat_history)

# --- Section-wise Guidance Generation Logic (Adapted for Flask) ---
def generate_specific_section(question: str, section: str, word_limit : int =150):

    """
    Generates the system prompt using the evaluation matrix and calls the LLM.
    This logic is directly adapted from the main_guidance_app.py.
    """

    if section.lower() == 'question_deconstruction':

        intro_wl_info = INTRODUCTION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]
        concl_wl_info = CONCLUSION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]

        system_prompt = f"""
        You are an expert UPSC Civil Services (Main) examiner for VisionIAS. Your task is to provide comprehensive,
        structured, and actionable Overall Answer Competence guidance on how a student should write a high-quality answer for a
        given UPSC Civil Services (Main) question.
        
        Strictly adhere to the following evaluation criteria and guidelines:

        **Overall Answer Competence (General Principles):**
        - Wholesome Nature: {get_evaluation_criteria('overall_answer_competence')['wholesome_nature']}
        - Clarity & Cohesion: {get_evaluation_criteria('overall_answer_competence')['clarity_cohesion']}
        - Adherence to Demand: {get_evaluation_criteria('overall_answer_competence')['adherence_to_demand']}
        - Examiner Perception: {get_evaluation_criteria('overall_answer_competence')['examiner_perception']}
        - Word Limit Adherence: {get_evaluation_criteria('overall_answer_competence')['word_limit_adherence']}

        Your output must strictly follow this structure using '###' for each main section heading.
        ## UPSC Civil Services (Main) Answer Guidance
        ### 1. Question Deconstruction
        Directive Word(s): **[Identify]**\nKeywords: **[Identify]**\nCore Demand: [Summarize what the question asks]

        ### 2. Value Addition Points
        [Suggest specific additional points like relevant articles, reports, committees, data, recent events, key terms that can enhance the answer.]

        ### 3. Common Pitfalls to Avoid
        [List 3-5 common mistakes relevant to the question or general UPSC Civil Services (Main) answer writing that students should avoid.]

        ### 4. Word Limit Suggestion
        For a {word_limit}-word answer:
            Introduction: {intro_wl_info['words']}
            Body: ~{word_limit - (int(intro_wl_info['words'].split('-')[0]) + int(concl_wl_info['words'].split('-')[0]))} words (approximate)
            Conclusion: {concl_wl_info['words']}

        """
        user_message = f"Please provide structured Overall Answer Competence writing guidance for the following UPSC Civil Services (Main) question (word limit: {word_limit} words):\n\nQuestion: {question}:\n\nSection: {section}"

        chat_history = [
            {"role": "user", "parts": [{"text": system_prompt}]},
            {"role": "user", "parts": [{"text": user_message}]}
        ]

        return call_gemini_api(chat_history)


    if section.lower() == "introduction":
        
        intro_wl_info = INTRODUCTION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]
        concl_wl_info = CONCLUSION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]

        system_prompt = f"""
        You are an expert UPSC Civil Services (Main) examiner for VisionIAS. Your task is to provide comprehensive,
        structured, and actionable introduction writing strategy on how a student should write a high-quality introduction for a 
        given UPSC Civil Services (Main) question.

        Strictly adhere to the following evaluation criteria and guidelines:

        **Introduction Competence:**
        - Aim & Purpose: {json.dumps(INTRODUCTION_COMPETENCE['aim_purpose'])}
        - Content Requirements: {json.dumps(INTRODUCTION_COMPETENCE['content_requirements'])}
        - Word Limit for {word_limit} words: {intro_wl_info['words']} (approx. {intro_wl_info['time_minutes']} minute)
        - Types of Introduction & Utilization: {json.dumps(INTRODUCTION_COMPETENCE['types'], indent=2)}
            - Note: Choose the most suitable type based on the question's nature.

        Your output must strictly follow this structure using '###' for each main section heading.
        ## UPSC Civil Services (Main) Answer Guidance

        ### 1. Introduction Strategy
        Recommended Type(s): [Suggest 1-2 types from the matrix with justification]
        Reasoning: [Explain why this type is suitable for the given question]
        Example Opening Hook (Approx. {intro_wl_info['words']}): "[Provide a concise example]"

        ### 2. Value Addition Points
        [Suggest specific additional points like relevant articles, reports, committees, data, recent events, key terms that can enhance the answer.]

        ### 3. Common Pitfalls to Avoid
        [List 3-5 common mistakes relevant to the question or general UPSC Civil Services (Main) answer writing that students should avoid.]

        ### 4. Word Limit Suggestion
        For a {word_limit}-word answer:
            Introduction: {intro_wl_info['words']}
            Body: ~{word_limit - (int(intro_wl_info['words'].split('-')[0]) + int(concl_wl_info['words'].split('-')[0]))} words (approximate)
            Conclusion: {concl_wl_info['words']}

        """

        user_message = f"Please provide structured introduction of the answer writing guidance for the following UPSC Civil Services (Main) question (word limit: {word_limit} words):\n\nQuestion: {question}:\n\nSection: {section}"

        chat_history = [
            {"role": "user", "parts": [{"text": system_prompt}]},
            {"role": "user", "parts": [{"text": user_message}]}
        ]

        return call_gemini_api(chat_history)
    
    if section.lower() == "body":

        intro_wl_info = INTRODUCTION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]
        concl_wl_info = CONCLUSION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]

        system_prompt = f"""
        You are an expert UPSC Civil Services (Main) examiner for VisionIAS. Your task is to provide comprehensive,
        structured, and actionable body writing strategy on how a student should write a high-quality body/key points/dimensions to cover for a 
        given UPSC Civil Services (Main) question.

        Strictly adhere to the following evaluation criteria and guidelines:

        **Body Competence (General Guidelines):**
        - Content Depth & Relevance: {BODY_COMPETENCE['content_depth_relevance']}
        - Multi-dimensionality: {BODY_COMPETENCE['multi_dimensionality']}
        - Evidence & Examples: {BODY_COMPETENCE['evidence_examples']}
        - Logical Flow: {BODY_COMPETENCE['logical_flow']}
        - Subheadings & Bullet Points: {BODY_COMPETENCE['subheadings_bullet_points']}

        Your output must strictly follow this structure using '###' for each main section heading.
        ## UPSC Civil Services (Main) Answer Guidance

        ### 1. Body - Key Dimensions/Points to Cover
        # [Use bullet points or subheadings to list 3-5 main aspects/arguments relevant to the question. For each, suggest brief content and potential examples/data/facts.]
        A. [Dimension/Point 1]: [Brief explanation, suggested content, e.g., facts/examples]
        B. [Dimension/Point 2]: [Brief explanation, suggested content, e.g., facts/examples]
        ... (add more points as relevant)

        ### 2. Value Addition Points
        [Suggest specific additional points like relevant articles, reports, committees, data, recent events, key terms that can enhance the answer.]

        ### 3. Common Pitfalls to Avoid
        [List 3-5 common mistakes relevant to the question or general UPSC Civil Services (Main) answer writing that students should avoid.]

        ### 4. Word Limit Suggestion
        For a {word_limit}-word answer:
            Introduction: {intro_wl_info['words']}
            Body: ~{word_limit - (int(intro_wl_info['words'].split('-')[0]) + int(concl_wl_info['words'].split('-')[0]))} words (approximate)
            Conclusion: {concl_wl_info['words']}

        """

        user_message = f"Please provide structured body of the answer writing guidance for the following UPSC Civil Services (Main) question (word limit: {word_limit} words):\n\nQuestion: {question}:\n\nSection: {section}"

        chat_history = [
            {"role": "user", "parts": [{"text": system_prompt}]},
            {"role": "user", "parts": [{"text": user_message}]}
        ]

        return call_gemini_api(chat_history)
    
    if section.lower() == "conclusion":

        intro_wl_info = INTRODUCTION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]
        concl_wl_info = CONCLUSION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]

        system_prompt = f"""
        You are an expert UPSC Civil Services (Main) examiner for VisionIAS. Your task is to provide comprehensive,
        structured, and actionable conclusion strategy guidance on how a student should write a high-quality conclusion to cover for a 
        given UPSC Civil Services (Main) question.

        Strictly adhere to the following evaluation criteria and guidelines:

        **Conclusion Competence:**
        - Aim & Purpose: {json.dumps(CONCLUSION_COMPETENCE['aim_purpose'])}
        - Word Limit for {word_limit} words: {concl_wl_info['words']} (approx. {concl_wl_info['time_minutes']} minute)
        - Types of Conclusion & Utilization: {json.dumps(CONCLUSION_COMPETENCE['types'], indent=2)}
            - Note: Choose the most suitable type based on the discussion in the body and question's directive.
        - Distinction from Way Forward: {json.dumps(CONCLUSION_COMPETENCE['distinction_from_way_forward'])}

        Your output must strictly follow this structure using '###' for each main section heading.
        ## UPSC Civil Services (Main) Answer Guidance

        ### 1. Conclusion Strategy
        Recommended Type(s): [Suggest 1-2 types from the matrix with justification]
        Reasoning: [Explain why this type is suitable]
        Example Closing Statement (Approx. {concl_wl_info['words']}): "[Provide a concise example]"

        ### 2. Value Addition Points
        [Suggest specific additional points like relevant articles, reports, committees, data, recent events, key terms that can enhance the answer.]

        ### 3. Common Pitfalls to Avoid
        [List 3-5 common mistakes relevant to the question or general UPSC Civil Services (Main) answer writing that students should avoid.]

        ### 4. Word Limit Suggestion
        For a {word_limit}-word answer:
            Introduction: {intro_wl_info['words']}
            Body: ~{word_limit - (int(intro_wl_info['words'].split('-')[0]) + int(concl_wl_info['words'].split('-')[0]))} words (approximate)
            Conclusion: {concl_wl_info['words']}

        """

        user_message = f"Please provide structured conclusion of the answer writing guidance for the following UPSC Civil Services (Main) question (word limit: {word_limit} words):\n\nQuestion: {question}:\n\nSection: {section}"

        chat_history = [
            {"role": "user", "parts": [{"text": system_prompt}]},
            {"role": "user", "parts": [{"text": user_message}]}
        ]

        return call_gemini_api(chat_history)

if __name__ == "__main__":
    logger.info("Prompts.py health Cheackup")
