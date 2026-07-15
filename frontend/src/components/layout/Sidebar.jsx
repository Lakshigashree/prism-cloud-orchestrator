import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  FiHome, 
  FiActivity, 
  FiTrendingUp, 
  FiSliders, 
  FiList, 
  FiBarChart2,
  FiCpu
} from 'react-icons/fi';
import './Sidebar.css';

const Sidebar = () => {
  const navItems = [
    { path: '/', icon: FiHome, label: 'Home' },
    { path: '/dashboard', icon: FiActivity, label: 'Dashboard' },
    { path: '/predictions', icon: FiTrendingUp, label: 'Predictions' },
    { path: '/decisions', icon: FiSliders, label: 'Decisions' },
    { path: '/audit', icon: FiList, label: 'Audit' },
    { path: '/results', icon: FiBarChart2, label: 'Results' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <FiCpu className="brand-icon" />
        <span className="brand-text">FORESIGHT</span>
      </div>
      
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => 
              `sidebar-link ${isActive ? 'active' : ''}`
            }
          >
            <item.icon className="link-icon" />
            <span className="link-label">{item.label}</span>
          </NavLink>
        ))}
      </nav>
      
      <div className="sidebar-footer">
        <div className="status-indicator">
          <span className="status-dot"></span>
          <span className="status-text">System Online</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;