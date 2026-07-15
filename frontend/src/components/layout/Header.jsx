import React from 'react';
import { FiMenu, FiBell, FiUser } from 'react-icons/fi';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-left">
        <button className="menu-toggle">
          <FiMenu size={24} />
        </button>
      </div>
      
      <div className="header-center">
        <div className="breadcrumb">
          <span>Cloud Orchestrator</span>
        </div>
      </div>
      
      <div className="header-right">
        <button className="header-btn">
          <FiBell size={20} />
          <span className="notification-dot"></span>
        </button>
        <button className="header-btn">
          <FiUser size={20} />
        </button>
      </div>
    </header>
  );
};

export default Header;