from utility.UPSC_evaluation_matrix import (
    get_evaluation_criteria,
    INTRODUCTION_COMPETENCE,
    CONCLUSION_COMPETENCE,
    BODY_COMPETENCE,
)
from utility.gemini import call_gemini_api
from utility.openai_handler import call_openai_api
import json
from utility.logger import logger


UPSC_GS_SYLLABUS = {
    "GS Paper 1": ["Indian Heritage and Culture", "History of the World and Society", "Geography of the World and Society"],
    "GS Paper 2": ["Governance", "Constitution", "Polity", "Social Justice", "International Relations"],
    "GS Paper 3": ["Technology", "Economic Development", "Bio-diversity", "Environment", "Security", "Disaster Management"],
    "GS Paper 4": ["Ethics, Integrity and Aptitude"]
}

FACT_CHECK_DIRECTIVE = """
Your primary role is to provide structural and conceptual guidance. 
AVOID providing specific data, statistics, or facts unless it is a well-established, stable piece of information (e.g., the year a law was passed). 
It is always better to suggest the TYPE of data a student should use (e.g., 'cite the latest NCRB report for conviction rates') rather than stating the data itself. If you must provide a fact, it must be accurate. 
Prioritize information from credible, official sources like government reports, parliamentary committees, and Supreme Court judgments.
"""

QUALITY_DIRECTIVE = """
Furthermore, adhere to these strict quality standards:
1.  **Precision:** All explanations must be precise, concise, and directly address the key point without unnecessary background information.
2.  **Example Quality:** All examples provided must be specific and value-adding. A good example is a concrete piece of data, a specific case study, a relevant committee name, or a landmark Supreme Court judgment. Avoid generic statements that just rephrase the main point.
3.  **Factual Accuracy:** Factual accuracy is critical. Be extra cautious with legal and constitutional provisions, especially regarding procedures like joint sittings of Parliament.
4.  **Clarity and Tone:** The language used must be simple and easy to understand, avoiding unnecessary jargon. The tone should be encouraging and interactive, as if a mentor is guiding a student.
"""



def generate_upsc_guidance_logic(question: str,category:str, word_limit: int = 150, optional_subject: str = None):
    """
    Generates the system prompt using the evaluation matrix and calls the LLM.
    This logic is directly adapted from your main_guidance_app.py.
    """

    CONTEXT_INSTRUCTION = ""
    if category == 'gs':
        CONTEXT_INSTRUCTION = f"""
        The user has specified this is a General Studies question. Your primary task is to analyze the question and map it to the specific subjects from the official UPSC syllabus provided below. You must identify one primary subject and can identify one or two secondary subjects if the question is inter-disciplinary.

        **Official GS Syllabus Topics:**
        {json.dumps(UPSC_GS_SYLLABUS, indent=2)}
        """
    elif category == 'optional' and optional_subject:
        CONTEXT_INSTRUCTION = f"The user has specified this is for their optional subject: {optional_subject}. Your primary task is to determine if the question relates more to Paper 1 (Foundations & Theories) or Paper 2 (Applied Concepts & Indian Context) of this optional."



    intro_wl_info = INTRODUCTION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]
    concl_wl_info = CONCLUSION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]

    system_prompt = f"""
    You are an expert UPSC Civil Services (Main) examiner from VisionIAS.{CONTEXT_INSTRUCTION}{QUALITY_DIRECTIVE}{FACT_CHECK_DIRECTIVE} Your task is to provide comprehensive,
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

# --- Section-wise Guidance Generation Logic ---
def generate_specific_section(question: str, section: str, category: str,word_limit : int =150, optional_subject: str = None):

    """
    Generates the system prompt using the evaluation matrix and calls the LLM.
    This logic is directly adapted from the main_guidance_app.py.
    """

    intro_wl_info = INTRODUCTION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]
    concl_wl_info = CONCLUSION_COMPETENCE['word_limit_time'][f"{word_limit}_words_question"]

    CONTEXT_INSTRUCTION = ""
    if category == 'gs':
        CONTEXT_INSTRUCTION = f"""
        The user has specified this is a General Studies question. 
        Your primary task is to analyze the question and map it to the specific subjects from the official UPSC syllabus provided below. 
        You must identify one primary subject and can identify one or two secondary subjects if the question is inter-disciplinary.

        **Official GS Syllabus Topics:**
        {json.dumps(UPSC_GS_SYLLABUS, indent=2)}
        """
    elif category == 'optional' and optional_subject:
        CONTEXT_INSTRUCTION = f"The user has specified this is for their optional subject: {optional_subject}. Your primary task is to determine if the question relates more to Paper 1 (Foundations & Theories) or Paper 2 (Applied Concepts & Indian Context) of this optional."


        
    if section.lower() == 'question_deconstruction':

        system_prompt = f"""
        You are an expert UPSC Civil Services (Main) examiner for VisionIAS.{CONTEXT_INSTRUCTION}{QUALITY_DIRECTIVE}{FACT_CHECK_DIRECTIVE} Your task is to provide comprehensive,
        structured, and actionable Overall Answer Competence guidance on how a student should write a high-quality answer for a given UPSC Civil Services (Main) question.
        
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
        Directive Word(s): **[Identify]**
        Keywords: **[Identify]**
        Keyword Explanation: [Provide a brief, one-sentence explanation for each identified directive words linking with the identified keywords, tailored to the context of the question.]
        Core Demand: [Summarize what the question asks]

        ### 2. Graphical Format Guidance
        Based on the question's nature, review the following presentation techniques and suggest 1-2 of the MOST relevant ones. For each suggestion, explain exactly how and where the student can use it in their answer.

        **List of Presentation Techniques:**
        - **Diagrams:** Simplify complex concepts for easier understanding.
        - **Maps:** Highlight locational aspects and geographical relevance.
        - **Tables:** Provide concise comparisons between different elements.
        - **Charts and Graphs:** Depict trends, growth, or statistical data.
        - **Schematics and Flowcharts:** Illustrate processes and frameworks clearly.
        - **Cyclical, Quadrilateral, and Triangular Geometric shapes:** Represent recurring or multi-dimensional concepts.
        - **Venn Diagrams:** Show relationships and intersections between topics.
        - **Timelines:** Display chronological sequence or policy evolution.
        - **Hub-and-Spoke Models:** Demonstrate interconnected elements or systems.
        - **Illustrative Art Forms:** Represent cultural and architectural aspects visually such as Stupa, Temple architecture etc.

        ### 3. Value Addition Points
        [Suggest specific additional points like relevant articles, reports, committees, data, recent events, key terms that can enhance the answer.]

        ### 4. Common Pitfalls to Avoid
        [List 3-5 common mistakes relevant to the question or general UPSC Civil Services (Main) answer writing that students should avoid.]

        ### 5. Word Limit Suggestion
        For a {word_limit}-word answer:
            Introduction: {intro_wl_info['words']}
            Body: ~{word_limit - (int(intro_wl_info['words'].split('-')[0]) + int(concl_wl_info['words'].split('-')[0]))} words (approximate)
            Conclusion: {concl_wl_info['words']}

        """


    elif section.lower() == "introduction":

        system_prompt = f"""
        You are an expert UPSC Civil Services (Main) examiner for VisionIAS.{CONTEXT_INSTRUCTION}{QUALITY_DIRECTIVE}{FACT_CHECK_DIRECTIVE} Your task is to provide comprehensive,
        structured, and actionable introduction writing strategy on how a student should write a high-quality introduction for a given UPSC Civil Services (Main) question.

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
        **Recommended Type:** [List 2-3 suitable types without detailed examples.]
          * **Most Suitable Type:** **[Name of the single best Intro Type]**
          * **Reasoning:** [Provide a one or two line explanation for why this specific type is the best choice for this question.]
          * **Example Hook (Approx. {intro_wl_info['words']}):** "[Provide a concise and impactful example hook. The example must be specific and directly relevant, not a generic restatement of the question's theme.]"

        """
    
    elif section.lower() == "body":

        system_prompt = f"""
        You are an expert UPSC Civil Services (Main) examiner for VisionIAS.{CONTEXT_INSTRUCTION}{QUALITY_DIRECTIVE}{FACT_CHECK_DIRECTIVE} Your task is to provide comprehensive,
        structured, and actionable body writing strategy on how a student should write a high-quality body/key points/dimensions to cover for a given UPSC Civil Services (Main) question.

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
        # [Use bullet points or subheadings to list 3-5 main aspects/arguments relevant to the question. For each, suggest brief content and a specific, value-adding example. The example should not be a simple restatement of the point, but should be a concrete piece of data, a specific case study, a relevant committee name, or a landmark Supreme Court judgment that substantiates the argument.]
        A. [Dimension/Point 1]: [Brief explanation, suggested content, e.g., facts/examples]
        B. [Dimension/Point 2]: [Brief explanation, suggested content, e.g., facts/examples]
        ... (add more points as relevant)
        
        """
    
    elif section.lower() == "conclusion":

        system_prompt = f"""
        You are an expert UPSC Civil Services (Main) examiner for VisionIAS.{CONTEXT_INSTRUCTION}{QUALITY_DIRECTIVE}{FACT_CHECK_DIRECTIVE} Your task is to provide comprehensive,
        structured, and actionable conclusion strategy guidance on how a student should write a high-quality conclusion to cover for a given UPSC Civil Services (Main) question.

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
        **Recommended Type:** [List 2-3 suitable types without detailed examples.]
          * **Most Suitable Type:** **[Name of the single best conclusion Type]**
          * **Reasoning:** [Provide a one line explanation for why this specific type is the best choice for this question.]
          * **Example Hook (Approx. {concl_wl_info['words']}):** "[Provide a concise and impactful closing statement. The example must be specific and directly relevant, not a generic summary.]"

        """
    
    else:
        logger.error(f"Invalid section requestion: {section}")
        raise ValueError(f"Guidance for section {section} is not defined!!")
    
    user_message = f"Please provide structured {section} of the answer writing guidance for the following UPSC Civil Services (Main) question (word limit: {word_limit} words):\n\nQuestion: {question}:\n\nSection: {section}"

    return call_openai_api(system_prompt,user_message)



def get_syllabus_subjects(question: str):
    """
    Instructs the AI to categorize a question and return a structured JSON list of subjects.
    """
    system_prompt = f"""
    You are an expert UPSC syllabus analyzer. Your task is to analyze the given UPSC Mains question and map it to the specific subjects from the official syllabus provided below. You must identify one primary subject and can identify one or two secondary subjects if the question is inter-disciplinary.

    **Official GS Syllabus Topics:**
    {json.dumps(UPSC_GS_SYLLABUS, indent=2)}
    
    Your output MUST be a valid JSON object containing a single key "subjects" which holds a list of the identified subject strings. Provide NO other text, explanation, or pleasantries.

    Example Input: "Discuss the impact of climate change on coastal ecosystems in India."
    Example Output: {{"subjects": ["GS Paper 1: Geography", "GS Paper 3: Environment & Ecology", "GS Paper 3: Disaster Management"]}}
    """
    
    user_prompt = f"Here is the question to analyze: \"{question}\""

    response_string = call_openai_api(system_prompt, user_prompt)
    
    try:
        # Clean up potential markdown code block fences
        cleaned_response = response_string.strip().replace('```json', '').replace('```', '')
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from categorization AI response: {response_string}")
        return {"error": "Failed to get a valid JSON response from the AI."}



if __name__ == "__main__":
    logger.info("Prompts.py health Cheackup")

