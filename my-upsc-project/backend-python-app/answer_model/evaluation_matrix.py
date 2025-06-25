# answer_model/evaluation_matrix.py

"""
This module defines the Ideal Answer Evaluation Matrix for UPSC Mains,
based on the "AW 2_Mentor's Reference Document (1).pdf".
It provides structured criteria for Introduction and Conclusion competence,
along with placeholders for other crucial aspects of a UPSC answer.
"""

# --- I. Overall Answer Competence (General Principles) ---
# These are high-level principles that apply across the entire answer.
OVERALL_ANSWER_COMPETENCE = {
    "wholesome_nature": "The answer should feel complete and well-rounded.",
    "clarity_cohesion": "Ideas should be logically connected and easy to follow.",
    "adherence_to_demand": "Directly addresses all parts of the question asked.",
    "examiner_perception": "Creates a positive impression of the student's capabilities and understanding.",
    "word_limit_adherence": "Stays within the specified total word limit for the entire answer.",
    "presentation_readability": "Good handwriting, neatness, and effective use of space contribute to readability."
}

# --- II. Introduction Competence ---
INTRODUCTION_COMPETENCE = {
    "aim_purpose": [
        "Get the reader immediately interested in the answer.",
        "Get the reader committed to read the answer.",
        "Lay out the demand of the question in more explicit terms.",
        "Indicate student expertise in the subject issue.",
        "Give background to the issues asked.",
        "Create a perception of good understanding of the problems.",
        "Help to make a smooth transition to the main demands of the question."
    ],
    "content_requirements": {
        "general": "Should generally give both the basic information about the issues and the central premise of the answer.",
        "multi_part_questions": "For questions with more than two parts, a common introduction should be written to create background for all aspects."
    },
    "word_limit_time": {
        "general_rule_percentage": "Ideally, not more than 15% of the total word limit.",
        "150_words_question": {
            "words": "20-25 words",
            "time_minutes": 1
        },
        "250_words_question": {
            "words": "35-40 words",
            "time_minutes": 1.5
        }
    },
    "types": [
        {
            "name": "Basic Info Type",
            "description": "Contains basic explanation, elaboration, or summarized significance of issues.",
            "utilization": [
                "Used for static questions with lesser connection to current affairs.",
                "History questions",
                "Geography questions",
                "Polity questions"
            ]
        },
        {
            "name": "Data Based Type",
            "description": "Highly impactful; demarcates comparison, relevance, and creates a strong perception of expertise. Requires accurate data.",
            "utilization": [
                "Mostly used in economic issues questions",
                "Mostly used in social issues questions",
                "Questions that require performance indicators"
            ],
            "data_collection_note": "Collecting data is difficult; collect on thematic issues (e.g., women empowerment, caste) or based on syllabus classification. Ensure basic understanding to avoid unnecessary data."
        },
        {
            "name": "Definition Type",
            "description": "Safest way to begin; lays down basics for further arguments. Requires a holistic definition without ambiguity.",
            "utilization": [
                "Most useful in Ethics questions",
                "Most useful in Geography questions",
                "Most useful in Science & Technology questions",
                "Most useful in Economic questions"
            ]
        },
        {
            "name": "Recent Event Type",
            "description": "Current event-based; defines the necessity of issues; reflects current understanding.",
            "utilization": [
                "Generally used for Social issues",
                "Generally used for Internal Security",
                "Generally used for International Relations",
                "Generally used for Economics"
            ]
        }
    ]
}

# --- III. Body Competence ---
# Note: The provided PDF primarily focuses on Intro/Conclusion.
# These points are general good practices for a UPSC answer body.
# Further detail can be added based on broader UPSC guidelines.
BODY_COMPETENCE = {
    "content_depth_relevance": "Addresses the core demands of the question with relevant facts, concepts, and arguments.",
    "multi_dimensionality": "Explores various facets of the issue (social, economic, political, environmental, ethical, etc.) where applicable.",
    "evidence_examples": "Supports arguments with appropriate examples, data, facts, and relevant information (e.g., reports, committees, constitutional articles, Supreme Court judgments).",
    "logical_flow": "Presents information in a coherent and structured manner.",
    "subheadings_bullet_points": "Uses subheadings and bullet points effectively for readability and organization."
}

# --- IV. Conclusion Competence ---
CONCLUSION_COMPETENCE = {
    "aim_purpose": [
        "Signifies understanding generated during argumentation.",
        "Needs to have a positive view (ideally, not negative, suitable for a public servant).",
        "Should not pose further questions.",
        "Creates a sense of closure.",
        "Adds value, especially if there's ambiguity in question demand."
    ],
    "word_limit_time": {
        "general_rule_percentage": "Similar to introduction, not more than 15% of the total word limit.",
        "150_words_question": {
            "words": "20-25 words",
            "time_minutes": 1
        },
        "250_words_question": {
            "words": "35-40 words",
            "time_minutes": 1.5
        }
    },
    "types": [
        {
            "name": "Summarized Conclusion",
            "description": "Mainly contains the idea discussed in the body in a summarized manner.",
            "utilization": [
                "Generally used to conclude scientific views (e.g., Geography questions)",
                "Generally used for Science & Technology questions"
            ]
        },
        {
            "name": "Balanced Conclusion",
            "description": "Makes the final inference from discussions, taking a balanced view, especially for arguments for/against.",
            "utilization": [
                "Used for questions with arguments for and against (e.g., 'Critically Comment' directive)",
                "History questions",
                "Polity questions",
                "Ethics questions"
            ]
        },
        {
            "name": "Reformist Conclusion",
            "description": "Provides solutions to issues/problems/challenges.",
            "utilization": [
                "Social issues questions",
                "Polity and Governance questions",
                "Economics questions"
            ]
        },
        {
            "name": "Futuristic Conclusion",
            "description": "Provides a vision for the future rather than just solutions for existing issues.",
            "utilization": [
                "Social issues questions",
                "History questions",
                "Polity questions",
                "Economics questions",
                "International Relations questions"
            ]
        }
    ],
    "distinction_from_way_forward": {
        "way_forward_nature": "Subset of conclusion, with several reformistic steps.",
        "conclusion_nature": "One grand reformistic vision; provides a sense of closure.",
        "explicitness": "Way forward can be explicit or implicit in a question; conclusion is implicit.",
        "usage_note": "Can use way forward as a conclusion in paucity of time and words, but it may not provide the same sense of closure."
    }
}

# --- Function to retrieve specific parts of the matrix ---
def get_evaluation_criteria(component: str = None):
    """
    Retrieves the complete evaluation matrix or a specific component.

    Args:
        component (str, optional): The specific component to retrieve (e.g., 'introduction', 'conclusion').
                                   Case-insensitive. Defaults to None (returns entire matrix).

    Returns:
        dict: The requested component or the entire evaluation matrix.
    """
    matrix = {
        "overall_answer_competence": OVERALL_ANSWER_COMPETENCE,
        "introduction_competence": INTRODUCTION_COMPETENCE,
        "body_competence": BODY_COMPETENCE,
        "conclusion_competence": CONCLUSION_COMPETENCE
    }

    if component:
        key = component.lower().replace(" ", "_")
        if key in matrix:
            return matrix[key]
        else:
            print(f"Warning: Component '{component}' not found. Returning full matrix.")
            return matrix
    return matrix

if __name__ == "__main__":
    # Example Usage:
    print("--- Full Evaluation Matrix ---")
    # import json
    # print(json.dumps(get_evaluation_criteria(), indent=2)) # Uncomment to print full matrix

    print("\n--- Introduction Competence Criteria ---")
    intro_criteria = get_evaluation_criteria("introduction_competence")
    print(f"General Word Limit Rule: {intro_criteria['word_limit_time']['general_rule_percentage']}")
    print("Introduction Types:")
    for type_info in intro_criteria['types']:
        print(f"  - {type_info['name']}: {type_info['description']} (Used for: {', '.join(type_info['utilization'])})")

    print("\n--- Conclusion Competence Criteria ---")
    concl_criteria = get_evaluation_criteria("conclusion_competence")
    print(f"Conclusion Aim: {concl_criteria['aim_purpose'][0]}")
    print("Conclusion Types:")
    for type_info in concl_criteria['types']:
        print(f"  - {type_info['name']}: {type_info['description']} (Used for: {', '.join(type_info['utilization'])})")

    print("\n--- Distinction: Conclusion vs. Way Forward ---")
    distinction = concl_criteria['distinction_from_way_forward']
    print(f"Way Forward Nature: {distinction['way_forward_nature']}")
    print(f"Conclusion Nature: {distinction['conclusion_nature']}")
