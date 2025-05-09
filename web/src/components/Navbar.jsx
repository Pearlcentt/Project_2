import React from 'react';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };
  
  return (
    <nav className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">HUST Assistant</h1>
        <button
          onClick={handleLogout}
          className="px-4 py-1 bg-white text-blue-600 rounded hover:bg-blue-100 transition duration-300"
        >
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;