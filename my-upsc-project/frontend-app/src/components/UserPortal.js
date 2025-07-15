// frontend-app/src/components/UserPortal.js

import React, { useState } from 'react';
import { callBackendApi, parseGuidanceMarkdown } from '../utils/commonUtils';
import ReactMarkdown from 'react-markdown';

const SECTION_OPTIONS = [
  { key: 'question_deconstruction', label: 'Question Deconstruction' },
  { key: 'introduction', label: 'Introduction Strategy' },
  { key: 'body', label: 'Body - Key Dimensions/Points to Cover' },
  { key: 'conclusion', label: 'Conclusion Strategy' }
];

const UPSC_OPTIONALS = [
  "Agriculture", "Animal Husbandry & Veterinary Science", "Anthropology", "Botany",
  "Chemistry", "Civil Engineering", "Commerce and Accountancy", "Economics",
  "Electrical Engineering", "Geography", "Geology", "History", "Law",
  "Management", "Mathematics", "Mechanical Engineering", "Medical Science",
  "Philosophy", "Physics", "Political Science & International Relations",
  "Psychology", "Public Administration", "Sociology", "Statistics", "Zoology"
];

const AccordionItem = ({ title, content, isOpen, toggleOpen }) => {
  const formattedContent = content
    .replace(/\*\*/g, '') 
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/Directive Word\(s\):/g, '**Directive Word(s):**')
    .replace(/Keywords:/g, '\n\n**Keywords:**')
    .replace(/Core Demand:/g, '\n\n**Core Demand:**')
    .replace(/Recommended Type\(s\):/g, '**Recommended Type(s):**')
    .replace(/Reasoning:/g, '\n\n**Reasoning:**')
    .replace(/Example Opening Hook/g, '\n\n**Example Opening Hook**')
    .replace(/Example Closing Statement/g, '\n\n**Example Closing Statement**')
    .replace(/Introduction:/g, '\n\n**Introduction:**')
    .replace(/Body:/g, '\n\n**Body:**')
    .replace(/Conclusion:/g, '\n\n**Conclusion:**')
    .replace(/\b(A\.)/g, '**$1**')
    .replace(/\b(B\.)/g, '\n\n**$1**')
    .replace(/\b(C\.)/g, '\n\n**$1**')
    .replace(/\b(D\.)/g, '\n\n**$1**')
    .replace(/\b(E\.)/g, '\n\n**$1**')
    .replace(/\* /g, '||BREAK||* ')
    .replace(/\n/g, ' ')
    .replace(/\|\|BREAK\|\|/g, '\n\n');

  return (
    <div className="border border-gray-300 rounded-lg overflow-hidden mb-4 shadow-sm">
      <button
        className="w-full text-left p-4 bg-gray-100 hover:bg-gray-200 font-semibold text-indigo-700 focus:outline-none transition-colors duration-200 flex justify-between items-center"
        onClick={toggleOpen}
      >
        <span>{title}</span>
        <span className="text-xl">{isOpen ? '−' : '+'}</span>
      </button>
      <div
        className={`transition-max-height duration-500 ease-in-out overflow-hidden ${
          isOpen ? 'max-h-screen' : 'max-h-0'
        }`}
      >
        <div className="p-6 border-t border-gray-200 bg-white">
          <div className="prose prose-indigo max-w-none text-gray-800">
            <ReactMarkdown>{formattedContent}</ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
};

const UserPortal = () => {
  const [question, setQuestion] = useState('');
  const [wordLimit, setWordLimit] = useState(150);
  const [selectedSection, setSelectedSection] = useState('');
  const [guidanceSections, setGuidanceSections] = useState([]);
  const [openSectionId, setOpenSectionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [copyFeedback, setCopyFeedback] = useState('');
  const [originalGuidance, setOriginalGuidance] = useState([]);
  const [targetLanguage, setTargetLanguage] = useState('en');
  const [isTranslating, setIsTranslating] = useState(false);
  const [rating, setRating] = useState('');
  const [comment, setComment] = useState('');
  const [category, setCategory] = useState('gs');
  const [optionalSubject, setOptionalSubject] = useState('');

  const submitFeedback = async () => {
    const latestSection = guidanceSections[guidanceSections.length - 1];
    if (!latestSection) {
      setError("No guidance has been generated yet to submit feedback for.");
      return;
    }
    if (!rating) {
      setError("Please provide a rating (1-10) before submitting.");
      return;
    }
    const feedbackPayload = {
      question: question,
      section: latestSection.title,
      guidance: latestSection.content,
      rating: Number(rating),
      comment: comment
    };
    try {
      const response = await callBackendApi("submit_feedback", feedbackPayload);
      alert(response.message || "Thank you for your feedback!");
      setRating('');
      setComment('');
      setError('');
    } catch (err) {
      setError(`Failed to submit feedback. ${err.message}`);
    }
  };

  const generateSectionGuidance = async () => {
    if (!question.trim() || !selectedSection || (category === 'optional' && !optionalSubject)) {
      setError('Please fill all required fields: Question, Category, Optional Subject (if applicable), and Section.');
      return;
    }
    setLoading(true);
    setError('');
    setCopyFeedback('');
    setOpenSectionId(null);
    try {
      const response = await callBackendApi('generate_section', {
        question: question,
        wordLimit: wordLimit,
        section: selectedSection,
        category: category,
        optional_subject: optionalSubject
      });
      const parsedSubSections = parseGuidanceMarkdown(response.guidance);
      const newSections = parsedSubSections.map((sec, index) => ({
        id: guidanceSections.length + index,
        title: sec.title,
        content: sec.content
      }));
      const newGuidanceArray = [...guidanceSections, ...newSections];
      setOriginalGuidance(newGuidanceArray);
      setGuidanceSections(newGuidanceArray);
      setTargetLanguage('en');
      setOpenSectionId(newSections.length > 0 ? newSections[0].id : null);
    } catch (err) {
      setError(`Failed to generate guidance: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };
  
  const handleLanguageChange = async (newLang) => {
    setTargetLanguage(newLang);
    if (newLang === 'en') {
      setGuidanceSections(originalGuidance);
      return;
    }
    if (originalGuidance.length === 0) return;
    setIsTranslating(true);
    setError('');
    try {
      let combinedText = "";
      originalGuidance.forEach(section => {
          combinedText += `### ${section.title}\n${section.content}\n\n`;
      });
      const response = await callBackendApi('translate', {
        text: combinedText, language: newLang,
      });
      const translatedText = response.translatedText;
      const parsedSections = parseGuidanceMarkdown(translatedText);
      const sectionsWithIds = parsedSections.map((sec, index) => ({ ...sec, id: index }));
      setGuidanceSections(sectionsWithIds);
    } catch (err) {
      setError(`Failed to translate guidance: ${err.message}. Please try again.`);
      setGuidanceSections(originalGuidance); 
    } finally {
      setIsTranslating(false);
    }
  };

  const handleReset = () => {
    setQuestion(''); setWordLimit(150); setSelectedSection('');
    setGuidanceSections([]); setOriginalGuidance([]);
    setOpenSectionId(null); setError(''); setCopyFeedback('');
    setTargetLanguage('en'); setRating(''); setComment('');
    setCategory('gs'); setOptionalSubject('');
  };

  const handleCopyGuidance = () => {
    let textToCopy = 'UPSC Mains Answer Guidance:\n\n';
    guidanceSections.forEach(section => {
      textToCopy += `### ${section.title}\n${section.content}\n\n`;
    });
    if (textToCopy.trim()) {
        const textarea = document.createElement('textarea');
        textarea.value = textToCopy;
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            setCopyFeedback('Copied to clipboard!');
        } catch (err) {
            console.error('Failed to copy text:', err);
            setCopyFeedback('Failed to copy. Please copy manually.');
        } finally {
            document.body.removeChild(textarea);
            setTimeout(() => setCopyFeedback(''), 2000);
        }
    }
  };

  return (
    <>
      <div className="space-y-6">
        <div>
          <label htmlFor="question" className="block text-lg font-semibold text-gray-700 mb-2">
            Enter UPSC Mains Question:
          </label>
          <textarea id="question" className="w-full p-4 border border-gray-300 rounded-lg"
            rows="5" placeholder="Type your UPSC Mains question here..." value={question}
            onChange={(e) => setQuestion(e.target.value)} />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-lg font-semibold text-gray-700 mb-2">Select Category:</label>
            <div className="flex gap-6 bg-gray-100 p-3 rounded-lg">
              <label className="inline-flex items-center cursor-pointer">
                <input type="radio" className="form-radio text-indigo-600 h-5 w-5" name="category" value="gs"
                  checked={category === 'gs'} onChange={() => setCategory('gs')} />
                <span className="ml-2 text-gray-700 font-medium">General Studies</span>
              </label>
              <label className="inline-flex items-center cursor-pointer">
                <input type="radio" className="form-radio text-indigo-600 h-5 w-5" name="category" value="optional"
                  checked={category === 'optional'} onChange={() => setCategory('optional')} />
                <span className="ml-2 text-gray-700 font-medium">Optional</span>
              </label>
            </div>
          </div>
          <div>
            <label className="block text-lg font-semibold text-gray-700 mb-2">Select Word Limit:</label>
            <div className="flex gap-6 bg-gray-100 p-3 rounded-lg">
              {[150, 250].map(limit => (
                <label key={limit} className="inline-flex items-center cursor-pointer">
                  <input type="radio" className="form-radio text-indigo-600 h-5 w-5" name="wordLimit" value={limit}
                    checked={wordLimit === limit} onChange={() => setWordLimit(limit)} />
                  <span className="ml-2 text-gray-700 font-medium">{limit} Words</span>
                </label>
              ))}
            </div>
          </div>
        </div>
        {category === 'optional' && (
          <div>
            <label htmlFor="optional-select" className="block text-lg font-semibold text-gray-700 mb-2">Select Optional Subject:</label>
            <select id="optional-select" value={optionalSubject} onChange={(e) => setOptionalSubject(e.target.value)}
              className="w-full rounded-md border-gray-300 shadow-sm px-4 py-3 text-gray-800 focus:ring-2 focus:ring-indigo-500">
              <option value="">-- Choose Your Optional --</option>
              {UPSC_OPTIONALS.map(opt => (<option key={opt} value={opt}>{opt}</option>))}
            </select>
          </div>
        )}
        <div>
          <label htmlFor="section-select" className="block text-lg font-semibold text-gray-700 mb-2">Guidance Section:</label>
          <select id="section-select" value={selectedSection} onChange={(e) => setSelectedSection(e.target.value)}
            className="w-full rounded-md border-gray-300 shadow-sm px-4 py-3 text-gray-800 focus:ring-2 focus:ring-indigo-500">
            <option value="">-- Select Section to Generate --</option>
            {SECTION_OPTIONS.map(opt => (<option key={opt.key} value={opt.key}>{opt.label}</option>))}
          </select>
        </div>
      </div>
      <button onClick={generateSectionGuidance}
        className={`w-full px-6 py-3 rounded-lg text-white font-bold text-lg transition-all duration-300 mt-6 ${
          (loading || !selectedSection || (category === 'optional' && !optionalSubject))
            ? 'bg-indigo-400 cursor-not-allowed'
            : 'bg-indigo-600 hover:bg-indigo-700'
        }`}
        disabled={loading || !selectedSection || (category === 'optional' && !optionalSubject)}>
        {loading ? 'Generating Guidance...' : 'Get Guidance for Section'}
      </button>

      {/* --- THIS ENTIRE SECTION WAS MISSING --- */}
      {error && (
        <div className="p-4 mt-4 bg-red-100 border border-red-400 text-red-700 rounded-lg" role="alert">
          {error}
        </div>
      )}

      {guidanceSections.length > 0 && (
        <div className="mt-8 space-y-6">
          <div className="p-6 bg-gray-50 rounded-xl border border-gray-200 shadow-inner space-y-4">
            <div className="flex justify-between items-center mb-4 flex-wrap gap-4">
              <h2 className="text-2xl font-bold text-indigo-700">Generated Guidance:</h2>
              <div className="flex items-center space-x-2">
                <label htmlFor="language-select" className="text-sm font-medium text-gray-600">Language:</label>
                <select id="language-select" value={targetLanguage} onChange={(e) => handleLanguageChange(e.target.value)}
                  className="rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                  disabled={isTranslating || loading}>
                  <option value="en">English</option><option value="hi">Hindi (हिन्दी)</option>
                </select>
                {isTranslating && <span className="text-sm text-indigo-600 animate-pulse">Translating...</span>}
              </div>
            </div>
            {guidanceSections.map((section) => (
              <AccordionItem key={section.id} title={section.title} content={section.content}
                isOpen={openSectionId === section.id} toggleOpen={() => setOpenSectionId(openSectionId === section.id ? null : section.id)} />
            ))}
          </div>

          <div className="mt-4 border-t pt-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-3">Rate the Latest Guidance</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="md:col-span-1">
                <label className="block text-sm font-medium mb-1">Your Rating (1–10):</label>
                <input type="number" min="1" max="10" className="border p-2 rounded w-full"
                  value={rating} onChange={(e) => setRating(e.target.value)} />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-1">Optional Comment:</label>
                <textarea className="border p-2 rounded w-full" placeholder="Your feedback helps us improve..."
                  value={comment} onChange={(e) => setComment(e.target.value)} />
              </div>
            </div>
            <button onClick={submitFeedback}
              className="bg-green-600 text-white px-4 py-2 rounded mt-3 font-semibold hover:bg-green-700">
              Submit Feedback
            </button>
          </div>

          <div className="flex justify-center mt-6 space-x-4 border-t pt-6">
            {copyFeedback && (
              <span className="text-sm text-green-600 self-center">{copyFeedback}</span>
            )}
            <button onClick={handleCopyGuidance}
              className="px-4 py-2 rounded-lg bg-blue-500 text-white font-semibold hover:bg-blue-600">
              Copy All Guidance
            </button>
            <button onClick={handleReset}
              className="px-4 py-2 rounded-lg bg-red-500 text-white font-semibold hover:bg-red-600">
              Reset
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default UserPortal;