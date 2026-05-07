import React from 'react';
import SimulationCanvas from './components/SimulationCanvas';
import './App.css';

function App() {
  return (
    <div className="app-container" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', backgroundColor: '#f9fafb' }}>
      <header style={{ backgroundColor: '#111827', color: 'white', padding: '1.5rem', textAlign: 'center', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
        <h1 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 600 }}>1D Numerical Diffusion Simulation</h1>
        <p style={{ margin: '0.5rem 0 0 0', color: '#9ca3af' }}>Physics-Informed Neural Network Portfolio</p>
      </header>
      
      <main style={{ flex: 1, padding: '2rem', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <SimulationCanvas />
      </main>
    </div>
  );
}

export default App;
