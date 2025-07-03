// frontend-app/src/utils/commonUtils.js

// Sample Questions Data (Centralized for PoC)
export const sampleQuestions = [
  { id: 1, text: "Discuss the impact of climate change on coastal ecosystems in India and suggest mitigation strategies.", topic: "Environment", wordLimit: 150 },
  { id: 2, text: "Analyse the role of digital literacy in fostering inclusive growth in rural India.", topic: "Social Issues", wordLimit: 150 },
  { id: 3, text: "Examine the challenges and opportunities for India in leveraging its demographic dividend.", topic: "Economy", wordLimit: 250 },
  { id: 4, text: "Critically evaluate the effectiveness of the Inter-State Council in promoting cooperative federalism in India.", topic: "Polity", wordLimit: 150 },
  { id: 5, text: "Highlight the ethical dilemmas associated with the rapid advancements in Artificial Intelligence and suggest a framework for responsible AI development.", topic: "Ethics", wordLimit: 250 },
];


// Evaluation Matrix data (copied from evaluation_matrix.py)
export const EVALUATION_MATRIX = {
  "overall_answer_competence": {
      "wholesome_nature": "The answer should feel complete and well-rounded.",
      "clarity_cohesion": "Ideas should be logically connected and easy to follow.",
      "adherence_to_demand": "Directly addresses all parts of the question asked.",
      "examiner_perception": "Creates a positive impression of the student's capabilities and understanding.",
      "word_limit_adherence": "Stays within the specified total word limit for the entire answer.",
      "presentation_readability": "Good handwriting, neatness, and effective use of space contribute to readability."
  },
  "introduction_competence": {
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
  },
  "body_competence": {
      "content_depth_relevance": "Addresses the core demands of the question with relevant facts, concepts, and arguments.",
      "multi_dimensionality": "Explores various facets of the issue (social, economic, political, environmental, ethical, etc.) where applicable.",
      "evidence_examples": "Supports arguments with appropriate examples, data, facts, and relevant information (e.g., reports, committees, constitutional articles, Supreme Court judgments).",
      "logical_flow": "Presents information in a coherent and structured manner.",
      "subheadings_bullet_points": "Uses subheadings and bullet points effectively for readability and organization."
  },
  "conclusion_competence": {
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
};

// Helper function to get nested criteria from the matrix
export const getCriteria = (componentPath) => {
  let current = EVALUATION_MATRIX;
  const path = componentPath.split('.');
  for (const key of path) {
    if (current && typeof current === 'object' && current.hasOwnProperty(key)) {
      current = current[key];
    } else {
      console.warn(`Path '${componentPath}' not found at key '${key}'`);
      return null;
    }
  }
  return current;
};

// Asynchronous function to call the FastAPI Backend
export const callBackendApi = async (endpoint, data) => {
  const backendUrl = `http://localhost:8000/${endpoint}`;

  try {
    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Backend API Error: ${response.status} ${response.statusText} - ${JSON.stringify(errorData)}`);
    }

    const result = await response.json();
    return result;

  } catch (e) {
    console.error("Error calling backend API:", e);
    throw e;
  }
};

// This parser will now handle a Markdown string with ### headings
export const parseGuidanceMarkdown = (markdownString) => {
  const sections = [];
  const headingRegex = /^(###\s+\d+\.\s+.*)$/gm;
  let match;
  let lastIndex = 0;

  while ((match = headingRegex.exec(markdownString)) !== null) {
    const heading = match[1];
    const startIndex = match.index;

    if (startIndex > lastIndex) {
      if (sections.length > 0) {
        sections[sections.length - 1].content = markdownString.substring(lastIndex, startIndex).trim();
      }
    }
    sections.push({ title: heading, content: '' });
    lastIndex = headingRegex.lastIndex;
  }

  if (sections.length > 0) {
    sections[sections.length - 1].content = markdownString.substring(lastIndex).trim();
  }

  return sections.map(section => ({
    title: section.title.replace(/###\s*/, ''), // Remove '### ' from title
    content: section.content.replace(new RegExp(`^${section.title.replace(/\./g, '\\.')}\\s*`), '').trim() // Remove title from content
  }));
};


// Common System Prompt generation logic - now requests Markdown output again
export const generateSystemPrompt = (wordLimit, introWlInfo, conclWlInfo) => {
  const commonHeaders = {
    overallAnswerCompetence: getCriteria('overall_answer_competence'),
    introductionCompetence: EVALUATION_MATRIX.introduction_competence,
    bodyCompetence: EVALUATION_MATRIX.body_competence,
    conclusionCompetence: EVALUATION_MATRIX.conclusion_competence
  };

  // Reverted to Markdown output with embedded HTML for Question Deconstruction
  return `
  You are an expert UPSC Mains examiner from Ajayvision. Your task is to provide comprehensive,
  structured, and actionable guidance on how a student should write a high-quality answer for a
  given UPSC Mains question.

  Strictly adhere to the following evaluation criteria and guidelines:

  **I. Overall Answer Competence (General Principles):**
  - Wholesome Nature: ${commonHeaders.overallAnswerCompetence.wholesome_nature}
  - Clarity & Cohesion: ${commonHeaders.overallAnswerCompetence.clarity_cohesion}
  - Adherence to Demand: ${commonHeaders.overallAnswerCompetence.adherence_to_demand}
  - Examiner Perception: ${commonHeaders.overallAnswerCompetence.examiner_perception}
  - Word Limit Adherence: ${commonHeaders.overallAnswerCompetence.word_limit_adherence}

  **II. Introduction Competence:**
  - Aim & Purpose: ${JSON.stringify(commonHeaders.introductionCompetence.aim_purpose)}
  - Content Requirements: ${JSON.stringify(commonHeaders.introductionCompetence.content_requirements)}
  - Word Limit for ${wordLimit} words: ${introWlInfo.words} (approx. ${introWlInfo.time_minutes} minute)
  - Types of Introduction & Utilization: ${JSON.stringify(commonHeaders.introductionCompetence.types, null, 2)}
      - Note: Choose the most suitable type based on the question's nature.

  **III. Body Competence (General Guidelines):**
  - Content Depth & Relevance: ${commonHeaders.bodyCompetence.content_depth_relevance}
  - Multi-dimensionality: ${commonHeaders.bodyCompetence.multi_dimensionality}
  - Evidence & Examples: ${commonHeaders.bodyCompetence.evidence_examples}
  - Logical Flow: ${commonHeaders.bodyCompetence.logical_flow}
  - Subheadings & Bullet Points: ${commonHeaders.bodyCompetence.subheadings_bullet_points}
  
  **IV. Conclusion Competence:**
  - Aim & Purpose: ${JSON.stringify(commonHeaders.conclusionCompetence.aim_purpose)}
  - Word Limit for ${wordLimit} words: ${conclWlInfo.words} (approx. ${conclWlInfo.time_minutes} minute)
  - Types of Conclusion & Utilization: ${JSON.stringify(commonHeaders.conclusionCompetence.types, null, 2)}
      - Note: Choose the most suitable type based on the discussion in the body and question's directive.
  - Distinction from Way Forward: ${JSON.stringify(commonHeaders.conclusionCompetence.distinction_from_way_forward)}

  Your output must strictly follow this structure using '###' for each main section heading.
  ## UPSC Mains Answer Guidance
  ### 1. Question Deconstruction
  <div class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-base items-start">
    <div class="font-semibold text-gray-700 whitespace-nowrap">Directive Word(s):</div> <div class="font-bold text-indigo-700">[Identify Directive Word(s)]</div>
    <div class="font-semibold text-gray-700 whitespace-nowrap">Keywords:</div> <div class="font-bold text-indigo-700">[Identify Keywords]</div>
    <div class="font-semibold text-gray-700 whitespace-nowrap">Core Demand:</div> <div class="font-normal text-gray-800">[Summarize what the question asks]</div>
  </div>

  ### 2. Introduction Strategy
  Recommended Type(s): [Suggest 1-2 types from the matrix with justification]
  Reasoning: [Explain why this type is suitable for the given question]
  Example Opening Hook (Approx. ${introWlInfo.words}): "[Provide a concise example]"

  ### 3. Body - Key Dimensions/Points to Cover
  [Use bullet points or subheadings to list 3-5 main aspects/arguments relevant to the question. For each, suggest brief content and potential examples/data/facts.]
  A. [Dimension/Point 1]: [Brief explanation, suggested content, e.g., facts/examples]
  B. [Dimension/Point 2]: [Brief explanation, suggested content, e.g., facts/examples]
  ... (add more points as relevant)

  ### 4. Conclusion Strategy
  Recommended Type(s): [Suggest 1-2 types from the matrix with justification]
  Reasoning: [Explain why this type is suitable]
  Example Closing Statement (Approx. ${conclWlInfo.words}): "[Provide a concise example]"

  ### 5. Value Addition Points
  [Suggest specific additional points like relevant articles, reports, committees, data, recent events, key terms that can enhance the answer.]

  ### 6. Common Pitfalls to Avoid
  [List 3-5 common mistakes relevant to the question or general UPSC answer writing that students should avoid.]

  ### 7. Word Limit Suggestion
  For a ${wordLimit}-word answer:
      Introduction: ${introWlInfo.words}
      Body: ~${wordLimit - (parseInt(introWlInfo.words.split('-')[0]) + parseInt(conclWlInfo.words.split('-')[0]))} words (approximate)
      Conclusion: ${conclWlInfo.words}
`;
};
