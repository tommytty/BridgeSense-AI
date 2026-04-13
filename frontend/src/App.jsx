import { useState } from 'react'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [detailsOpen, setDetailsOpen] = useState(false)
  const [profilerOpen, setProfilerOpen] = useState(false)
  const [criteriaOpen, setCriteriaOpen] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    setSelectedFile(file)
    setPreviewUrl(URL.createObjectURL(file))
    analyzeFile(file)
  }

  const analyzeFile = async (file) => {
    setIsLoading(true)
    setError(null)
    
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Analysis failed')
      }
      
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }
  const handleReset = () => {
    setSelectedFile(null)
    setPreviewUrl(null)
    setResult(null)
    setError(null)
    setDetailsOpen(false)
    setProfilerOpen(false)
    setCriteriaOpen(false)
  }
   
  return (
    
    <div className="app">
      <h1>BridgeSense AI</h1>

      {isLoading && (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Analyzing bridge...</p>
        </div>
      )}

      {error && !isLoading && (
        <div className="error-state">
          <p>Error: {error}</p>
          <button onClick={() => { setError(null); setSelectedFile(null); }}>
            Try Again
          </button>
        </div>
      )}

      {!isLoading && !result && !error && (
        <label className="upload-zone">
          <input 
            type="file" 
            accept="image/*"
            onChange={handleFileChange}
            hidden
          />
          <div className="upload-zone-content">
            <p>Drop a bridge image or click to upload</p>
          </div>
        </label>
      )}


      {result && !isLoading && (
        <div className="results">
          <button className="back-button" onClick={handleReset}>
            ← ANALYZE ANOTHER BRIDGE
          </button>
          <div className="result-image-section">
            <img src={previewUrl} alt="Uploaded bridge" className="bridge-image" />
          </div>
          
          <div className="identification-card">
            <div className="id-label">IDENTIFICATION</div>
            <h2 className="bridge-name">{result.profile.bridge_name}</h2>
            <p className="bridge-location">{result.profile.bridge_location}</p>
            <div className="confidence">
              <span className="confidence-label">CONFIDENCE: </span>
              <span className="confidence-value">{result.profile.identification_confidence}</span>
            </div>
          </div>

          <div className="score-card">
            <div className="score-display">
              <div className="score-label">OVERALL UDP SCORE</div>
              <div className="score-value">
                {result.analysis.overall_score}
                <span className="score-max">/5</span>
              </div>
            </div>
          </div>
          <div className="details-section">
            <button 
              className="details-toggle"
              onClick={() => setDetailsOpen(!detailsOpen)}
            >
              <span>{detailsOpen ? 'HIDE DETAILS' : 'SHOW DETAILS'}</span>
              <span className="toggle-icon">{detailsOpen ? '−' : '+'}</span>
            </button>
            
            {detailsOpen && (
              <div className="details-content">
                {result.analysis.principles.map((principle) => (
                  <div key={principle.id} className="principle-card">
                    <div className="principle-header">
                      <div className="principle-id">P{principle.id}</div>
                      <div className="principle-name">{principle.name}</div>
                      <div className="principle-score">
                        {principle.score}<span className="score-max-small">/5</span>
                      </div>
                    </div>
                    <p className="principle-reasoning">{principle.reasoning}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="recommendations-card">
            <div className="section-label">RECOMMENDATIONS</div>
            <ul className="recommendations-list">
              {result.analysis.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
          <div className="profiler-section">
            <button 
              className="profiler-toggle"
              onClick={() => setProfilerOpen(!profilerOpen)}
            >
              <span>{profilerOpen ? 'HIDE PROFILER DATA' : 'VIEW PROFILER DATA'}</span>
              <span className="toggle-icon-small">{profilerOpen ? '−' : '+'}</span>
            </button>
            
            {profilerOpen && (
              <div className="profiler-content">
                <div className="profiler-grid">
                  <div className="profiler-field">
                    <div className="field-label">BRIDGE TYPE</div>
                    <p className="field-value">{result.profile.bridge_type}</p>
                  </div>
                  <div className="profiler-field">
                    <div className="field-label">TYPICAL USERS</div>
                    <p className="field-value">{result.profile.typical_users}</p>
                  </div>
                  <div className="profiler-field">
                    <div className="field-label">CONTEXT</div>
                    <p className="field-value">{result.profile.context_summary}</p>
                  </div>
                  <div className="profiler-field">
                    <div className="field-label">REASONING</div>
                    <p className="field-value">{result.profile.reasoning}</p>
                  </div>
                </div>
                <div className="criteria-nested">
                  <button 
                    className="criteria-toggle"
                    onClick={() => setCriteriaOpen(!criteriaOpen)}
                  >
                    <span>{criteriaOpen ? 'HIDE GENERATED CRITERIA' : 'VIEW GENERATED CRITERIA'}</span>
                    <span className="toggle-icon-small">{criteriaOpen ? '−' : '+'}</span>
                  </button>
                  
                  {criteriaOpen && (
                    <div className="criteria-content">
                      {result.profile.principles.map((principle) => (
                        <div key={principle.id} className="criteria-principle">
                          <div className="criteria-principle-header">
                            <span className="criteria-id">P{principle.id}</span>
                            <span className="criteria-name">{principle.name}</span>
                          </div>
                          <ul className="criteria-list">
                            {principle.bridge_criteria.map((criterion, idx) => (
                              <li key={idx}>{criterion}</li>
                            ))}
                          </ul>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )

}

export default App