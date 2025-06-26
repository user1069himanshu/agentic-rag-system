// frontend-app/src/components/AdminPortal.js

import React, { useState } from 'react';

// Sample Questions Data (In-memory for PoC) - This is local to AdminPortal for its demo
const sampleQuestions = [
  { id: 1, text: "Discuss the impact of climate change on coastal ecosystems in India and suggest mitigation strategies.", topic: "Environment" },
  { id: 2, text: "Analyse the role of digital literacy in fostering inclusive growth in rural India.", topic: "Social Issues" },
  { id: 3, text: "Examine the challenges and opportunities for India in leveraging its demographic dividend.", topic: "Economy" },
  { id: 4, text: "Critically evaluate the effectiveness of the Inter-State Council in promoting cooperative federalism in India.", topic: "Polity" },
  { id: 5, text: "Highlight the ethical dilemmas associated with the rapid advancements in Artificial Intelligence and suggest a framework for responsible AI development.", topic: "Ethics" },
];

const AdminPortal = () => { // Removed setCurrentPortal from props
  const [adminKeyInput, setAdminKeyInput] = useState('');
  const [adminKeyError, setAdminKeyError] = useState('');
  const ADMIN_POC_KEY = "ajayvisionadmin"; // Hardcoded admin key for PoC

  const [questionsInMemory, setQuestionsInMemory] = useState(sampleQuestions);
  const [editingQuestion, setEditingQuestion] = useState(null); // null or { id, text, topic }
  const [newQuestionText, setNewQuestionText] = useState('');
  const [newQuestionTopic, setNewQuestionTopic] = useState('');

  const handleAdminLogin = () => {
    if (adminKeyInput === ADMIN_POC_KEY) {
      // In a real app, you'd set a token/cookie here
      setAdminKeyError(''); // Clear any previous error
    } else {
      setAdminKeyError('Invalid Admin Key');
    }
  };

  const handleEditQuestion = (id) => {
    const q = questionsInMemory.find(q => q.id === id);
    if (q) {
      setEditingQuestion(q);
      setNewQuestionText(q.text);
      setNewQuestionTopic(q.topic);
    }
  };

  const handleSaveQuestion = () => {
    if (!newQuestionText.trim() || !newQuestionTopic.trim()) {
      alert('Question text and topic cannot be empty.');
      return;
    }
    if (editingQuestion) {
      setQuestionsInMemory(questionsInMemory.map(q =>
        q.id === editingQuestion.id ? { ...q, text: newQuestionText, topic: newQuestionTopic } : q
      ));
      alert('Question updated successfully (in-memory)!');
    } else {
      const newId = questionsInMemory.length > 0 ? Math.max(...questionsInMemory.map(q => q.id)) + 1 : 1;
      setQuestionsInMemory([...questionsInMemory, { id: newId, text: newQuestionText, topic: newQuestionTopic }]);
      alert('Question added successfully (in-memory)!');
    }
    setEditingQuestion(null);
    setNewQuestionText('');
    setNewQuestionTopic('');
  };

  const handleDeleteQuestion = (id) => {
    if (window.confirm('Are you sure you want to delete this question (in-memory)?')) {
      setQuestionsInMemory(questionsInMemory.filter(q => q.id !== id));
      alert('Question deleted successfully (in-memory)!');
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-indigo-800">Admin Portal</h2>
        {/* Removed the "Go to User Portal" button */}
      </div>

      {adminKeyInput !== ADMIN_POC_KEY && ( // Show key input if not verified
        <div className="space-y-4">
          <label htmlFor="adminKey" className="block text-lg font-semibold text-gray-700">
            Enter Admin Key:
          </label>
          <input
            id="adminKey"
            type="password"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 text-gray-800"
            placeholder="***********"
            value={adminKeyInput}
            onChange={(e) => setAdminKeyInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') handleAdminLogin();
            }}
          />
          <button
            onClick={handleAdminLogin}
            className="w-full px-6 py-3 rounded-lg bg-indigo-600 text-white font-bold text-lg hover:bg-indigo-700 transition-colors"
          >
            Verify Key
          </button>
          {adminKeyError && (
            <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg text-sm" role="alert">
              {adminKeyError}
            </div>
          )}
        </div>
      )}

      {adminKeyInput === ADMIN_POC_KEY && ( // Show admin content if key is correct
        <div className="space-y-8 mt-8">
          <h3 className="text-2xl font-bold text-gray-800 border-b pb-2 mb-4">Manage Questions (In-memory PoC)</h3>
          
          {/* Add/Edit Question Form */}
          <div className="p-6 bg-white rounded-lg shadow-md border border-gray-200 space-y-4">
            <h4 className="text-xl font-semibold text-indigo-700 mb-3">{editingQuestion ? 'Edit Question' : 'Add New Question'}</h4>
            <input
              type="text"
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 text-gray-800"
              placeholder="Question Text"
              value={newQuestionText}
              onChange={(e) => setNewQuestionText(e.target.value)}
            />
            <input
              type="text"
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 text-gray-800"
              placeholder="Topic (e.g., Polity, Economy)"
              value={newQuestionTopic}
              onChange={(e) => setNewQuestionTopic(e.target.value)}
            />
            <button
              onClick={handleSaveQuestion}
              className="w-full px-6 py-3 rounded-lg bg-green-600 text-white font-bold hover:bg-green-700 transition-colors"
            >
              {editingQuestion ? 'Save Changes' : 'Add Question'}
            </button>
            {editingQuestion && (
              <button
                onClick={() => {
                  setEditingQuestion(null);
                  setNewQuestionText('');
                  setNewQuestionTopic('');
                }}
                className="w-full px-6 py-3 mt-2 rounded-lg bg-gray-400 text-white font-bold hover:bg-gray-500 transition-colors"
              >
                Cancel Edit
              </button>
            )}
          </div>

          {/* List Questions */}
          <div className="p-6 bg-white rounded-lg shadow-md border border-gray-200">
            <h4 className="text-xl font-semibold text-indigo-700 mb-3">Current Questions</h4>
            <ul className="divide-y divide-gray-200">
              {questionsInMemory.map(q => (
                <li key={q.id} className="py-4 flex flex-col sm:flex-row justify-between items-start sm:items-center">
                  <div>
                    <p className="text-gray-900 font-medium">Q{q.id}. {q.text}</p>
                    <span className="text-sm text-gray-500">Topic: {q.topic}</span>
                  </div>
                  <div className="flex space-x-2 mt-3 sm:mt-0">
                    <button
                      onClick={() => handleEditQuestion(q.id)}
                      className="px-3 py-1 text-sm rounded-md bg-blue-500 text-white hover:bg-blue-600 transition-colors"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDeleteQuestion(q.id)}
                      className="px-3 py-1 text-sm rounded-md bg-red-500 text-white hover:bg-red-600 transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          <h3 className="text-2xl font-bold text-gray-800 border-b pb-2 mb-4">Manage Users (Dummy PoC)</h3>
          <div className="p-6 bg-white rounded-lg shadow-md border border-gray-200">
            <h4 className="text-xl font-semibold text-indigo-700 mb-3">Registered Users</h4>
            <ul className="divide-y divide-gray-200">
              <li className="py-2 text-gray-700">User ID: dummy_user_12345 (Student)</li>
              <li className="py-2 text-gray-700">User ID: another_dummy_user (Student)</li>
              <li className="py-2 text-gray-700">User ID: example_user_9876 (Student)</li>
            </ul>
            <p className="mt-4 text-sm text-gray-500">Note: User data is simulated in this Proof of Concept.</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPortal;
