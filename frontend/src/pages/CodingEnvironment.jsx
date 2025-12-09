import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { testsAPI } from '../api/tests';
import './CodingEnvironment.css';

const LANGUAGES = {
  python: 'python',
  javascript: 'javascript',
  java: 'java',
  cpp: 'cpp',
};

const DEFAULT_CODE = {
  python: '# Write your code here\n\ndef solution():\n    pass\n',
  javascript: '// Write your code here\n\nfunction solution() {\n    \n}\n',
  java: '// Write your code here\n\npublic class Solution {\n    public static void main(String[] args) {\n        \n    }\n}\n',
  cpp: '// Write your code here\n\n#include <iostream>\nusing namespace std;\n\nint main() {\n    \n    return 0;\n}\n',
};

const CodingEnvironment = () => {
  const { testId } = useParams();
  const navigate = useNavigate();
  const [test, setTest] = useState(null);
  const [code, setCode] = useState(DEFAULT_CODE.python);
  const [language, setLanguage] = useState('python');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [timeLeft, setTimeLeft] = useState(null);
  const [isTestActive, setIsTestActive] = useState(true);
  const autoSaveTimerRef = useRef(null);

  useEffect(() => {
    loadTest();
    return () => {
      if (autoSaveTimerRef.current) {
        clearInterval(autoSaveTimerRef.current);
      }
    };
  }, [testId]);

  useEffect(() => {
    if (test && test.time_limit) {
      setTimeLeft(test.time_limit * 60);
    }
  }, [test]);

  useEffect(() => {
    // Don't start timer until timeLeft is initialized
    if (timeLeft === null) {
      return;
    }

    if (timeLeft <= 0) {
      setIsTestActive(false);
      handleSubmit();
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          setIsTestActive(false);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

  useEffect(() => {
    // Auto-save every 30 seconds
    autoSaveTimerRef.current = setInterval(() => {
      if (code) {
        saveProgress();
      }
    }, 30000);

    return () => {
      if (autoSaveTimerRef.current) {
        clearInterval(autoSaveTimerRef.current);
      }
    };
  }, [code, testId]);

  const loadTest = async () => {
    try {
      const data = await testsAPI.getTest(testId);
      setTest(data);
      
      // Try to load saved code
      try {
        const savedData = await testsAPI.getSavedCode(testId);
        if (savedData.code) {
          setCode(savedData.code);
          if (savedData.language) {
            setLanguage(savedData.language);
          }
        }
      } catch (err) {
        console.log('No saved code found');
      }
    } catch (err) {
      console.error('Failed to load test:', err);
    } finally {
      setLoading(false);
    }
  };

  const saveProgress = async () => {
    try {
      await testsAPI.saveProgress(testId, code);
      console.log('Progress saved');
    } catch (err) {
      console.error('Failed to save progress:', err);
    }
  };

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
    if (!code || code === DEFAULT_CODE[language]) {
      setCode(DEFAULT_CODE[newLanguage]);
    }
  };

  const handleRunCode = async () => {
    setRunning(true);
    setOutput('Running...');
    
    try {
      const result = await testsAPI.executeCode({
        code,
        language,
        test_id: testId,
      });
      
      setOutput(result.output || result.error || 'Execution completed');
    } catch (err) {
      setOutput(`Error: ${err.response?.data?.error || err.message}`);
    } finally {
      setRunning(false);
    }
  };

  const handleSubmit = async () => {
    if (!window.confirm('Are you sure you want to submit your solution?')) {
      return;
    }

    try {
      const result = await testsAPI.submitCode(testId, {
        code,
        language,
      });
      
      alert(`Submission successful! Score: ${result.score || 'Pending'}`);
      navigate('/dashboard');
    } catch (err) {
      alert(`Submission failed: ${err.response?.data?.error || err.message}`);
    }
  };

  const formatTime = (seconds) => {
    if (seconds === null) return '--:--';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return <div className="loading-container">Loading test...</div>;
  }

  if (!test) {
    return <div className="error-container">Test not found</div>;
  }

  return (
    <div className="coding-environment">
      <header className="coding-header">
        <div className="header-left">
          <button onClick={() => navigate('/dashboard')} className="btn-back">
            ← Back
          </button>
          <h1>{test.name}</h1>
        </div>
        
        <div className="header-center">
          <div className={`timer ${timeLeft < 300 ? 'timer-warning' : ''}`}>
            <svg className="timer-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {formatTime(timeLeft)}
          </div>
        </div>
        
        <div className="header-right">
          <select 
            value={language} 
            onChange={(e) => handleLanguageChange(e.target.value)}
            className="language-select"
            disabled={!isTestActive}
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="java">Java</option>
            <option value="cpp">C++</option>
          </select>
          
          <button 
            onClick={handleRunCode} 
            disabled={running || !isTestActive}
            className="btn-run"
          >
            {running ? 'Running...' : 'Run Code'}
          </button>
          
          <button 
            onClick={handleSubmit}
            disabled={!isTestActive}
            className="btn-submit"
          >
            Submit
          </button>
        </div>
      </header>

      <div className="coding-main">
        <div className="problem-panel">
          <div className="panel-header">
            <h2>Problem Description</h2>
            <span className={`difficulty-badge difficulty-${test.difficulty.toLowerCase()}`}>
              {test.difficulty}
            </span>
          </div>
          <div className="problem-content">
            <p>{test.description}</p>
            
            {test.test_cases && test.test_cases.length > 0 && (
              <div className="test-cases">
                <h3>Sample Test Cases</h3>
                {test.test_cases.slice(0, 2).map((tc, index) => (
                  <div key={index} className="test-case">
                    <div className="test-case-label">Example {index + 1}:</div>
                    <div className="test-case-io">
                      <div>
                        <strong>Input:</strong>
                        <pre>{tc.input_data}</pre>
                      </div>
                      <div>
                        <strong>Expected Output:</strong>
                        <pre>{tc.expected_output}</pre>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="editor-panel">
          <div className="panel-header">
            <h2>Code Editor</h2>
            <span className="auto-save-info">Auto-saves every 30s</span>
          </div>
          <div className="editor-wrapper">
            <Editor
              height="calc(100% - 200px)"
              language={language}
              value={code}
              onChange={(value) => setCode(value || '')}
              theme="vs-dark"
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 4,
                readOnly: !isTestActive,
              }}
            />
          </div>
          
          <div className="output-panel">
            <div className="output-header">
              <h3>Output</h3>
            </div>
            <pre className="output-content">
              {output || 'Run your code to see the output here...'}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodingEnvironment;
