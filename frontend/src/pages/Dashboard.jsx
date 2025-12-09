import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { testsAPI } from '../api/tests';
import './Dashboard.css';

const Dashboard = () => {
  const [tests, setTests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    loadTests();
  }, []);

  const loadTests = async () => {
    try {
      const data = await testsAPI.getAllTests();
      setTests(data);
    } catch (err) {
      setError('Failed to load tests');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleStartTest = (testId) => {
    navigate(`/test/${testId}`);
  };

  const getDifficultyClass = (difficulty) => {
    return `difficulty-${difficulty.toLowerCase()}`;
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Coding Tests Platform</h1>
        <div className="user-info">
          <span>Welcome, {user?.username || 'Candidate'}!</span>
          <button onClick={handleLogout} className="btn-logout">Logout</button>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-content">
          <h2>Available Tests</h2>
          
          {error && <div className="error-message">{error}</div>}
          
          {loading ? (
            <div className="loading">Loading tests...</div>
          ) : tests.length === 0 ? (
            <div className="no-tests">No tests available at the moment.</div>
          ) : (
            <div className="tests-grid">
              {tests.map((test) => (
                <div key={test.id} className="test-card">
                  <div className="test-header">
                    <h3>{test.name}</h3>
                    <span className={`difficulty-badge ${getDifficultyClass(test.difficulty)}`}>
                      {test.difficulty}
                    </span>
                  </div>
                  
                  <p className="test-description">{test.description}</p>
                  
                  <div className="test-info">
                    <div className="info-item">
                      <svg className="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span>{test.time_limit} minutes</span>
                    </div>
                  </div>
                  
                  <button 
                    onClick={() => handleStartTest(test.id)} 
                    className="btn-start"
                  >
                    Start Test
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
