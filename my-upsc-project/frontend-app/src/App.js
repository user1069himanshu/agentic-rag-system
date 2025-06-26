// frontend-app/src/App.js

import React, { useState, useEffect } from 'react';
import UserPortal from './components/UserPortal'; // Import UserPortal
import AdminPortal from './components/AdminPortal'; // Import AdminPortal

const App = () => {
  // Determine which portal to show based on URL
  const [currentPath, setCurrentPath] = useState(window.location.pathname);

  useEffect(() => {
    // Listen for path changes (useful if using browser's back/forward buttons)
    const handlePopState = () => {
      setCurrentPath(window.location.pathname);
    };
    window.addEventListener('popstate', handlePopState);
    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, []);

  const renderPortal = () => {
    if (currentPath.startsWith('/admin')) {
      // Removed setCurrentPortal prop
      return <AdminPortal />;
    } else {
      // Removed setCurrentPortal prop
      return <UserPortal />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100 flex items-center justify-center p-4 font-inter">
      <div className="w-full max-w-4xl bg-white rounded-xl shadow-lg p-8 space-y-8">
        <h1 className="text-4xl font-extrabold text-center text-indigo-800 mb-6">
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-indigo-600">Ajayvision</span> UPSC Mains Guidance PoC
        </h1>
        {renderPortal()}
      </div>
    </div>
  );
};

export default App;
