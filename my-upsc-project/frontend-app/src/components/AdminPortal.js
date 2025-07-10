// frontend-app/src/components/AdminPortal.js

import React, { useState, useEffect } from 'react';

const sampleQuestions = [
  { id: 1, text: "Discuss the impact of climate change on coastal ecosystems in India and suggest mitigation strategies.", topic: "Environment" },
  { id: 2, text: "Analyse the role of digital literacy in fostering inclusive growth in rural India.", topic: "Social Issues" },
  { id: 3, text: "Examine the challenges and opportunities for India in leveraging its demographic dividend.", topic: "Economy" },
];

const FeedbackList = ({ title, feedbackItems, onModerate, onEdit, onSave, onCancel, editingId, editText, setEditText }) => {
  if (!feedbackItems || feedbackItems.length === 0) {
    return <p className="text-gray-500">No {title.toLowerCase()} feedback found.</p>;
  }
  return (
    <div>
      <h3 className="text-2xl font-bold text-gray-800 border-b pb-2 mb-4">{title}</h3>
      <ul className="space-y-4">
        {feedbackItems.map((fb) => (
          <li key={fb.id} className="border p-4 rounded-lg shadow-sm bg-white">
            <p className="text-sm text-gray-500">Q: {fb.question}</p>
            <p className="mt-2"><strong>Guidance for:</strong> {fb.section}</p>
            <p><strong>Rating:</strong> <span className="font-bold text-indigo-700">{fb.rating}/10</span></p>
            {editingId === fb.id ? (
              <div className="my-2">
                <label className="font-semibold">Edit Comment:</label>
                <textarea
                  className="w-full border p-2 rounded mt-1"
                  value={editText}
                  onChange={(e) => setEditText(e.target.value)}
                />
              </div>
            ) : (
              <p><strong>Comment:</strong> {fb.comment || "No comment."}</p>
            )}
            {onModerate && (
              <div className="mt-3">
                {editingId === fb.id ? (
                  <>
                    <button onClick={() => onSave(fb.id, "approve")} className="bg-blue-500 text-white px-3 py-1 rounded mr-2 hover:bg-blue-600">Save & Approve</button>
                    <button onClick={() => onSave(fb.id, "reject")} className="bg-orange-500 text-white px-3 py-1 rounded mr-2 hover:bg-orange-600">Save & Reject</button>
                    <button onClick={onCancel} className="bg-gray-400 text-white px-3 py-1 rounded hover:bg-gray-500">Cancel</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => onModerate(fb.id, "approve")} className="bg-green-500 text-white px-3 py-1 rounded mr-2 hover:bg-green-600">Approve</button>
                    <button onClick={() => onModerate(fb.id, "reject")} className="bg-red-500 text-white px-3 py-1 rounded mr-2 hover:bg-red-600">Reject</button>
                    <button onClick={() => onEdit(fb)} className="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600">Edit</button>
                  </>
                )}
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

const AdminPortal = () => {
  const [adminKeyInput, setAdminKeyInput] = useState('');
  const [adminKeyError, setAdminKeyError] = useState('');
  const ADMIN_POC_KEY = "ajayvisionadmin";
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [pendingFeedback, setPendingFeedback] = useState([]);
  const [approvedFeedback, setApprovedFeedback] = useState([]);
  const [rejectedFeedback, setRejectedFeedback] = useState([]);
  const [approvedCount, setApprovedCount] = useState(0);
  const [rejectedCount, setRejectedCount] = useState(0);
  const [viewingStatus, setViewingStatus] = useState('pending');
  const [editingFeedbackId, setEditingFeedbackId] = useState(null);
  const [editedCommentText, setEditedCommentText] = useState("");
  const [questions, setQuestions] = useState(sampleQuestions);
  const [isEditingQuestion, setIsEditingQuestion] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState({ id: null, text: '', topic: '' });

  const handleAdminLogin = () => {
    if (adminKeyInput === ADMIN_POC_KEY) {
      setIsAuthenticated(true);
      setAdminKeyError('');
    } else {
      setAdminKeyError('Invalid Admin Key');
    }
  };
  
  useEffect(() => {
    if (isAuthenticated) {
      fetchFeedbackByStatus('pending');
      fetchModeratedStats();
    }
  }, [isAuthenticated]);

  const fetchModeratedStats = async () => {
    try {
      const res = await fetch("http://localhost:8000/feedback_stats");
      if (!res.ok) throw new Error("Failed to fetch stats");
      const data = await res.json();
      setApprovedCount(data.approved);
      setRejectedCount(data.rejected);
    } catch(err) {
      console.error(err);
      setAdminKeyError("Could not fetch feedback stats from the backend.");
    }
  };

  const fetchFeedbackByStatus = async (status) => {
    try {
      const endpoint = status === 'pending' ? 'pending_feedback' : `feedback_by_status?status=${status}`;
      const res = await fetch(`http://localhost:8000/${endpoint}`);
      if (!res.ok) throw new Error(`Failed to fetch ${status} feedback`);
      const data = await res.json();
      if (status === 'pending') setPendingFeedback(data);
      else if (status === 'approve') setApprovedFeedback(data);
      else if (status === 'reject') setRejectedFeedback(data);
    } catch (err) {
      console.error(err);
      setAdminKeyError(`Could not connect to backend to fetch ${status} feedback.`);
    }
  };

  const moderateFeedback = async (id, action) => {
    const feedbackItem = pendingFeedback.find(fb => fb.id === id);
    if (feedbackItem) {
      await handleSaveAndModerate(id, action, feedbackItem.comment);
    }
  };
  
  const handleEditClick = (feedback) => {
    setEditingFeedbackId(feedback.id);
    setEditedCommentText(feedback.comment);
  };

  const handleCancelEdit = () => {
    setEditingFeedbackId(null);
    setEditedCommentText("");
  };

  const handleSaveAndModerate = async (id, action, commentToSave) => {
    try {
      await fetch(`http://localhost:8000/moderate_feedback?id=${id}&action=${action}`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment: commentToSave })
      });
      setEditingFeedbackId(null);
      fetchFeedbackByStatus(viewingStatus); // Re-fetch the current view
      fetchModeratedStats(); // Always update stats
    } catch(err) {
      console.error(err);
      setAdminKeyError("Failed to moderate feedback.");
    }
  };

  const handleViewChange = (status) => {
    setViewingStatus(status);
    fetchFeedbackByStatus(status);
  };
  
  const handleQuestionInputChange = (e) => {
    const { name, value } = e.target;
    setCurrentQuestion({ ...currentQuestion, [name]: value });
  };

  const handleSaveQuestion = () => {
    if (!currentQuestion.text.trim() || !currentQuestion.topic.trim()) {
      alert("Question text and topic cannot be empty.");
      return;
    }
    if (isEditingQuestion) {
      setQuestions(questions.map(q => q.id === currentQuestion.id ? currentQuestion : q));
    } else {
      setQuestions([...questions, { ...currentQuestion, id: Date.now() }]);
    }
    handleCancelQuestionEdit();
  };

  const handleEditQuestionClick = (question) => {
    setIsEditingQuestion(true);
    setCurrentQuestion(question);
  };

  const handleDeleteQuestion = (id) => {
    if (window.confirm("Are you sure you want to delete this question?")) {
      setQuestions(questions.filter(q => q.id !== id));
    }
  };

  const handleCancelQuestionEdit = () => {
    setIsEditingQuestion(false);
    setCurrentQuestion({ id: null, text: '', topic: '' });
  };

  const renderCurrentView = () => {
    switch (viewingStatus) {
      case 'approve':
        return <FeedbackList title="Approved Feedback" feedbackItems={approvedFeedback} />;
      case 'reject':
        return <FeedbackList title="Rejected Feedback" feedbackItems={rejectedFeedback} />;
      default:
        return <FeedbackList title="Pending Feedback" feedbackItems={pendingFeedback} onModerate={moderateFeedback} onEdit={handleEditClick} onSave={(id, action) => handleSaveAndModerate(id, action, editedCommentText)} onCancel={handleCancelEdit} editingId={editingFeedbackId} editText={editedCommentText} setEditText={setEditedCommentText} />;
    }
  };

  return (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-indigo-800">Admin Portal</h2>
      {!isAuthenticated ? (
        <div className="space-y-4">
          <label htmlFor="adminKey" className="block text-lg font-semibold text-gray-700">Enter Admin Key:</label>
          <input id="adminKey" type="password" className="w-full p-3 border border-gray-300 rounded-lg"
            placeholder="***********" value={adminKeyInput} onChange={(e) => setAdminKeyInput(e.target.value)}
            onKeyPress={(e) => { if (e.key === 'Enter') handleAdminLogin(); }} />
          <button onClick={handleAdminLogin} className="w-full px-6 py-3 rounded-lg bg-indigo-600 text-white font-bold text-lg hover:bg-indigo-700">
            Verify Key
          </button>
          {adminKeyError && <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg text-sm">{adminKeyError}</div>}
        </div>
      ) : (
        <div className="space-y-8 mt-8">
          <div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <button onClick={() => handleViewChange('approve')} className="text-left bg-green-100 text-green-800 p-4 rounded-lg shadow hover:bg-green-200 transition-colors">
                <p className="font-semibold">Approved Feedback</p>
                <p className="text-3xl font-bold">{approvedCount}</p>
              </button>
              <button onClick={() => handleViewChange('reject')} className="text-left bg-red-100 text-red-800 p-4 rounded-lg shadow hover:bg-red-200 transition-colors">
                <p className="font-semibold">Rejected Feedback</p>
                <p className="text-3xl font-bold">{rejectedCount}</p>
              </button>
              <button onClick={() => handleViewChange('pending')} className="text-left bg-yellow-100 text-yellow-800 p-4 rounded-lg shadow hover:bg-yellow-200 transition-colors">
                <p className="font-semibold">Pending Feedback</p>
                <p className="text-3xl font-bold">{pendingFeedback.length}</p>
              </button>
            </div>
            <div className="mt-6">
              {renderCurrentView()}
            </div>
          </div>
          <div className="mt-8 border-t pt-6">
            <h3 className="text-2xl font-bold text-gray-800 border-b pb-2 mb-4">Manage Questions (In-memory PoC)</h3>
            <div className="p-4 border rounded-lg bg-white shadow-sm mb-6">
              <h4 className="font-semibold text-lg mb-3">{isEditingQuestion ? 'Edit Question' : 'Add New Question'}</h4>
              <div className="space-y-4">
                <textarea name="text" placeholder="Question Text" className="w-full p-2 border rounded"
                  value={currentQuestion.text} onChange={handleQuestionInputChange} rows={3} />
                <input type="text" name="topic" placeholder="Topic (e.g., Polity, Economy)" className="w-full p-2 border rounded"
                  value={currentQuestion.topic} onChange={handleQuestionInputChange} />
                <div className="flex gap-4">
                  <button onClick={handleSaveQuestion} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                    {isEditingQuestion ? 'Update Question' : 'Save Question'}
                  </button>
                  {isEditingQuestion && (
                    <button onClick={handleCancelQuestionEdit} className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">
                      Cancel
                    </button>
                  )}
                </div>
              </div>
            </div>
            <h4 className="font-semibold text-lg mb-3">Existing Questions</h4>
            <ul className="space-y-3">
              {questions.map(q => (
                <li key={q.id} className="border p-3 rounded-md bg-gray-50 flex justify-between items-center flex-wrap gap-2">
                  <div className="flex-grow">
                    <p className="font-medium">{q.text}</p>
                    <p className="text-sm text-indigo-600 bg-indigo-100 px-2 py-1 rounded-full inline-block mt-1">{q.topic}</p>
                  </div>
                  <div className="flex gap-2 flex-shrink-0">
                    <button onClick={() => handleEditQuestionClick(q)} className="text-sm text-blue-600 hover:underline">Edit</button>
                    <button onClick={() => handleDeleteQuestion(q.id)} className="text-sm text-red-600 hover:underline">Delete</button>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPortal;