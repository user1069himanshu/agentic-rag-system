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

// This is a simple accordion item component for cleaner code
const AccordionItem = ({ title, content, isOpen, toggleOpen }) => {
  
  // FINAL (Robust): Comprehensive formatting logic for ALL sections and patterns
  const formattedContent = content
    // 1. First, remove any inconsistent bolding from the AI
    .replace(/\*\*/g, '') 
    
    // 2. Then, apply our own consistent formatting for "Label: Value" patterns
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

    // 3. Add formatting for "Enumerated List" patterns using a robust word boundary (\b)
    // This finds the letters A., B., etc. reliably.
    .replace(/\b(A\.)/g, '**$1**')      // Bold A. without adding a preceding newline
    .replace(/\b(B\.)/g, '\n\n**$1**')  // Add a newline and bold B.
    .replace(/\b(C\.)/g, '\n\n**$1**')
    .replace(/\b(D\.)/g, '\n\n**$1**')
    .replace(/\b(E\.)/g, '\n\n**$1**');


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
            {/* Use the final 'formattedContent' variable here */}
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


  const generateSectionGuidance = async () => {
    if (!question.trim() || !selectedSection) {
      setError('Please enter a UPSC question and select a section.');
      return;
    }

    setLoading(true);
    setError('');
    setGuidanceSections([]);
    setCopyFeedback('');
    setOpenSectionId(null);

    try {
      const response = await callBackendApi('generate_section', {
        question: question,
        wordLimit: wordLimit,
        section: selectedSection,
      });

      setGuidanceSections(prev => [
        ...prev,
        {
          id: prev.length,
          title: SECTION_OPTIONS.find(opt => opt.key === selectedSection)?.label || selectedSection,
          content: response.guidance
        }
      ]);
      setSelectedSection('');
      setOpenSectionId(guidanceSections.length);

      const result = response.guidance;
      const parsedSections = parseGuidanceMarkdown(result);
      const sectionsWithIds = parsedSections.map((sec, index) => ({ ...sec, id: index }));
      
      setOriginalGuidance(sectionsWithIds);
      setGuidanceSections(sectionsWithIds);

      setTargetLanguage('en'); 
      setOpenSectionId(sectionsWithIds.length > 0 ? sectionsWithIds[0].id : null);

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
        text: combinedText,
        language: newLang,
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
    setQuestion('');
    setWordLimit(150);
    setSelectedSection('');
    setGuidanceSections([]);
    setOriginalGuidance([]);
    setOpenSectionId(null);
    setError('');
    setCopyFeedback('');
    setTargetLanguage('en');
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
      {/* Question Input Section */}
      <div className="space-y-4">
        <label htmlFor="question" className="block text-lg font-semibold text-gray-700">
          Enter UPSC Mains Question:
        </label>
        <textarea
          id="question"
          className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 resize-y min-h-[120px] text-gray-800"
          rows="5"
          placeholder="Type your UPSC Mains question here..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        ></textarea>
      </div>

      <div className="mt-6">
        <div>
          <label className="block text-lg font-semibold text-gray-700 mb-1">Select Word Limit:</label>
          <div className="flex gap-6">
            {[150, 250].map(limit => (
              <label key={limit} className="inline-flex items-center cursor-pointer">
                <input
                  type="radio"
                  className="form-radio text-indigo-600 h-5 w-5"
                  name="wordLimit"
                  value={limit}
                  checked={wordLimit === limit}
                  onChange={() => setWordLimit(limit)}
                />
                <span className="ml-2 text-gray-700 font-medium">{limit} Words</span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-lg font-semibold text-gray-700 mb-1">Which Section would you like guidance on?</label>
          <select
            value={selectedSection}
            onChange={(e) => setSelectedSection(e.target.value)}
            className="w-full rounded-md border-gray-300 px-4 py-2 text-gray-800"
          >
            <option value="">-- Select Section --</option>
            {SECTION_OPTIONS.map(opt => (
              <option key={opt.key} value={opt.key}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
      </div>
      

      

      <button
        onClick={generateSectionGuidance}
        className={`w-full px-6 py-3 rounded-lg text-white font-bold text-lg transition-all duration-300 ${
          loading
            ? 'bg-indigo-400 cursor-not-allowed animate-pulse'
            : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 hover:shadow-md'
        }`}
        disabled={loading}
      >
        {loading ? 'Generating Guidance...' : 'Get Guidance'}
      </button>

      {error && (
        <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg" role="alert">
          {error}
        </div>
      )}

      {/* Guidance Accordion Display Section */}
      {guidanceSections.length > 0 && (
        <div className="mt-8 p-6 bg-gray-50 rounded-xl border border-gray-200 shadow-inner space-y-4">
          
          <div className="flex justify-between items-center mb-4 flex-wrap gap-4">
            <h2 className="text-2xl font-bold text-indigo-700">UPSC Mains Guidance:</h2>
            
            <div className="flex items-center space-x-2">
              <label htmlFor="language-select" className="text-sm font-medium text-gray-600">Language:</label>
              <select
                id="language-select"
                value={targetLanguage}
                onChange={(e) => handleLanguageChange(e.target.value)}
                className="rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                disabled={isTranslating || loading}
              >
                <option value="en">English</option>
                <option value="hi">Hindi (हिन्दी)</option>
                <option value="bn">Bengali (বাংলা)</option>
                <option value="ta">Tamil (தமிழ்)</option>
                <option value="te">Telugu (తెలుగు)</option>
                <option value="mr">Marathi (मराठी)</option>
              </select>
              {isTranslating && <span className="text-sm text-indigo-600 animate-pulse">Translating...</span>}
            </div>
          </div>
          
          {guidanceSections.map((section) => (
            <AccordionItem
              key={section.id}
              title={section.title}
              content={section.content}
              isOpen={openSectionId === section.id}
              toggleOpen={() => setOpenSectionId(openSectionId === section.id ? null : section.id)}
            />
          ))}

          <div className="flex justify-center mt-4 space-x-4">
            {copyFeedback && (
               <span className="text-sm text-green-600 self-center">{copyFeedback}</span>
            )}
            <button
              onClick={() => handleCopyGuidance()}
              className="px-4 py-2 rounded-lg bg-blue-500 text-white font-semibold hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Copy All Guidance
            </button>
            <button
              onClick={handleReset}
              className="px-4 py-2 rounded-lg bg-red-500 text-white font-semibold hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              Start New Question
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default UserPortal;