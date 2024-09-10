import React from 'react'
import './App.css'
import FileUpload from './components/FileUpload'
import GraphComponent from './components/Graph'

function App() {
  return (
    <div className="app-container">
      <div className="file-upload-section">
        <FileUpload />
      </div>
      <div className="graph-section">
        <h2>Graph Section</h2>
        <GraphComponent />
      </div>
    </div>
  )
}

export default App