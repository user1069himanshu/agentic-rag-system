// frontend-app/src/components/AdminPortal.js

import React, { useState, useEffect } from 'react'; // <-- Import useEffect

// Sample Questions Data (In-memory for PoC) - This is local to AdminPortal for its demo
const sampleQuestions = [
  { id: 1, text: "Discuss the impact of climate change on coastal ecosystems in India and suggest mitigation strategies.", topic: "Environment" },
  { id: 2, text: "Analyse the role of digital literacy in fostering inclusive growth in rural India.", topic: "Social Issues" },
  { id: 3, text: "Examine the challenges and opportunities for India in leveraging its demographic dividend.", topic: "Economy" },
  { id: 4, text: "Critically evaluate the effectiveness of the Inter-State Council in promoting cooperative federalism in India.", topic: "Polity" },
  { id: 5, text: "Highlight the ethical dilemmas associated with the rapid advancements in Artificial Intelligence and suggest a framework for responsible AI development.", topic: "Ethics" },
];

const AdminPortal = () => {
  const [adminKeyInput, setAdminKeyInput] = useState('');
  const [adminKeyError, setAdminKeyError] = useState('');
  const ADMIN_POC_KEY = "ajayvisionadmin";
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [pendingFeedback, setPendingFeedback] = useState([]);
  const [approvedCount, setApprovedCount] = useState(0);
  const [rejectedCount, setRejectedCount] = useState(0);
  const [questionsInMemory, setQuestionsInMemory] = useState(sampleQuestions);
  const [editingQuestion, setEditingQuestion] = useState(null); 
  const [newQuestionText, setNewQuestionText] = useState('');
  const [newQuestionTopic, setNewQuestionTopic] = useState('');
  const [editingFeedbackId, setEditingFeedbackId] = useState(null);
  const [editedCommentText, setEditedCommentText] = useState("");

  
  const handleAdminLogin = () => {
    if (adminKeyInput === ADMIN_POC_KEY) {
      setIsAuthenticated(true); 
      setAdminKeyError('');
    } else {
      setAdminKeyError('Invalid Admin Key');
      setIsAuthenticated(false);
    }
  };
  
 
  useEffect(() => {
    if (isAuthenticated) {
      console.log("Admin authenticated. Fetching data...");
      fetchPendingFeedback();
      fetchModeratedStats();
    }
  }, [isAuthenticated]); // The dependency array ensures this runs when isAuthenticated changes


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

  // --- These functions are now called by useEffect ---
  const fetchPendingFeedback = async () => {
    try {
        const res = await fetch("http://localhost:8000/pending_feedback");
        if (!res.ok) throw new Error("Failed to fetch pending feedback");
        const data = await res.json();
        setPendingFeedback(data);
    } catch(err) {
        console.error(err);
        setAdminKeyError("Could not connect to backend to fetch feedback.");
    }
  };

  const fetchModeratedStats = async () => {
    try {
        const res = await fetch("http://localhost:8000/feedback_stats");
        if (!res.ok) throw new Error("Failed to fetch stats");
        const data = await res.json();
        setApprovedCount(data.approved);
        setRejectedCount(data.rejected);
    } catch(err) {
        console.error(err);
    }
  };

  const moderateFeedback = async (id, action) => {
    await fetch(`http://localhost:8000/moderate_feedback?id=${id}&action=${action}`, {
      method: "POST"
    });
    // Re-fetch data to update the UI
    fetchPendingFeedback();
    fetchModeratedStats();
  };


  const handleEditClick = (feedback) => {
    setEditingFeedbackId(feedback.id);
    setEditedCommentText(feedback.comment);
  };

  const handleCancelEdit = () => {
    setEditingFeedbackId(null);
    setEditedCommentText("");
  };

  const handleSaveAndModerate = async (id, action) => {
    // We will now send the edited comment to the backend
    await fetch(`http://localhost:8000/moderate_feedback?id=${id}&action=${action}`, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comment: editedCommentText }) // Send the edited comment
    });
    
    setEditingFeedbackId(null); // Exit edit mode
    fetchPendingFeedback();
    fetchModeratedStats();
  };




  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-indigo-800">Admin Portal</h2>
      </div>

      {!isAuthenticated ? ( // Show login form if not authenticated
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
      ) : ( // Show admin content if authenticated
        <div className="space-y-8 mt-8">
          <div className="flex gap-6">
            <div className="bg-green-100 text-green-800 p-4 rounded shadow">
              <p className="font-semibold">Approved Feedback</p>
              <p className="text-2xl font-bold">{approvedCount}</p>
            </div>
            <div className="bg-red-100 text-red-800 p-4 rounded shadow">
              <p className="font-semibold">Rejected Feedback</p>
              <p className="text-2xl font-bold">{rejectedCount}</p>
            </div>
          </div>

          <h3 className="text-2xl font-bold text-gray-800 border-b pb-2 mb-4">Pending Feedback</h3>
          {pendingFeedback.length === 0 ? (
            <p className="text-gray-500">No unverified feedback.</p>
          ) : (
            <ul className="space-y-4">
              {pendingFeedback.map((fb) => (
                <li key={fb.id} className="border p-4 rounded-lg shadow-sm bg-white">
                  {/* ... (other feedback details) ... */}
                  <p><strong>Rating:</strong> <span className="font-bold text-indigo-700">{fb.rating}/10</span></p>
                  
                  {/* --- NEW: Conditional rendering for editing comments --- */}
                  {editingFeedbackId === fb.id ? (
                    <div className="my-2">
                      <label className="font-semibold">Edit Comment:</label>
                      <textarea
                        className="w-full border p-2 rounded mt-1"
                        value={editedCommentText}
                        onChange={(e) => setEditedCommentText(e.target.value)}
                      />
                    </div>
                  ) : (
                    <p><strong>Comment:</strong> {fb.comment || "No comment."}</p>
                  )}

                  <div className="mt-3">
                    {editingFeedbackId === fb.id ? (
                      <>
                        <button onClick={() => handleSaveAndModerate(fb.id, "approve")} className="bg-blue-500 text-white px-3 py-1 rounded mr-2 hover:bg-blue-600">Save & Approve</button>
                        <button onClick={() => handleSaveAndModerate(fb.id, "reject")} className="bg-orange-500 text-white px-3 py-1 rounded mr-2 hover:bg-orange-600">Save & Reject</button>
                        <button onClick={handleCancelEdit} className="bg-gray-400 text-white px-3 py-1 rounded hover:bg-gray-500">Cancel</button>
                      </>
                    ) : (
                      <>
                        <button onClick={() => moderateFeedback(fb.id, "approve")} className="bg-green-500 text-white px-3 py-1 rounded mr-2 hover:bg-green-600">Approve</button>
                        <button onClick={() => moderateFeedback(fb.id, "reject")} className="bg-red-500 text-white px-3 py-1 rounded mr-2 hover:bg-red-600">Reject</button>
                        <button onClick={() => handleEditClick(fb)} className="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600">Edit</button>
                      </>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          )}
          {/* ... (rest of the component) ... */}
        </div>
      )}
    </div>
  );
};
// Note: You would also need to update the `moderateFeedback` function to match the `handleSaveAndModerate` pattern
// if you want to approve/reject without editing. For simplicity, this example combines saving with moderation.
export default AdminPortal;