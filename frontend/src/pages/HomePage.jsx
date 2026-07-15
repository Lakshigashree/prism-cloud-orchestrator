import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  FiActivity, 
  FiTrendingUp, 
  FiSliders, 
  FiBarChart2,
  FiArrowRight,
  FiCpu,
  FiCloud,
  FiZap
} from 'react-icons/fi';
import './HomePage.css';

const HomePage = () => {
  const features = [
    {
      icon: FiActivity,
      title: 'Live Monitoring',
      description: 'Real-time traffic, carbon, and performance metrics',
    },
    {
      icon: FiTrendingUp,
      title: 'Intelligent Predictions',
      description: 'LSTM-based forecasting for proactive decisions',
    },
    {
      icon: FiSliders,
      title: 'Multi-Objective Decision',
      description: 'Optimize cost, carbon, and latency simultaneously',
    },
    {
      icon: FiBarChart2,
      title: 'Audit & Insights',
      description: 'Complete history with impact analysis',
    },
  ];

  return (
    <div className="home-page">
      <motion.section 
        className="hero"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="hero-content">
          <div className="hero-badge">
            <FiCpu />
            <span>Adaptive Resource Intelligence</span>
          </div>
          <h1>
            FORESIGHT
            <span className="hero-subtitle">
              Forecast-Oriented Resource & Emission Sustainability Intelligence
            </span>
          </h1>
          <p className="hero-description">
            Intelligent cloud orchestration that optimizes cost, carbon emissions, 
            and performance using hybrid twin modeling and multi-objective reinforcement learning.
          </p>
          <div className="hero-actions">
            <Link to="/dashboard" className="btn-primary">
              Launch Dashboard
              <FiArrowRight />
            </Link>
            <Link to="/results" className="btn-secondary">
              View Results
            </Link>
          </div>
        </div>
        <div className="hero-visual">
          <div className="visual-grid">
            <div className="grid-item" style={{ background: 'rgba(96, 165, 250, 0.1)' }}>
              <FiCloud />
              <span>Cloud</span>
            </div>
            <div className="grid-item" style={{ background: 'rgba(52, 211, 153, 0.1)' }}>
              <FiZap />
              <span>Energy</span>
            </div>
            <div className="grid-item" style={{ background: 'rgba(167, 139, 250, 0.1)' }}>
              <FiActivity />
              <span>Performance</span>
            </div>
            <div className="grid-item" style={{ background: 'rgba(244, 114, 182, 0.1)' }}>
              <FiTrendingUp />
              <span>Optimize</span>
            </div>
          </div>
        </div>
      </motion.section>

      <motion.section 
        className="features"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <h2>How It Works</h2>
        <div className="features-grid">
          {features.map((feature, index) => (
            <motion.div 
              key={index}
              className="feature-card"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
            >
              <feature.icon className="feature-icon" />
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </motion.section>

      <motion.section 
        className="cta-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.5 }}
      >
        <div className="cta-content">
          <h2>Ready to Optimize Your Cloud?</h2>
          <p>Explore the full capabilities of FORESIGHT and start making smarter decisions.</p>
          <Link to="/dashboard" className="btn-primary">
            Get Started
            <FiArrowRight />
          </Link>
        </div>
      </motion.section>
    </div>
  );
};

export default HomePage;