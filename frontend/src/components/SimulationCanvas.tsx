import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Play, Pause, RotateCcw } from 'lucide-react';
import './SimulationCanvas.css';

// Helper to map temperature to a color (blue for 20, red for 100)
const getTemperatureColor = (temp: number) => {
  const minTemp = 20;
  const maxTemp = 100;
  const t = Math.max(0, Math.min(1, (temp - minTemp) / (maxTemp - minTemp)));
  // Interpolate from blue (0,0,255) to red (255,0,0)
  const r = Math.round(t * 255);
  const b = Math.round((1 - t) * 255);
  return `rgb(${r}, 0, ${b})`;
};

const RodSegment = ({ position, color, length }: { position: [number, number, number], color: string, length: number }) => {
  return (
    <mesh position={position}>
      <cylinderGeometry args={[0.5, 0.5, length, 16]} />
      <meshStandardMaterial color={color} />
    </mesh>
  );
};

const SimulationCanvas = () => {
  const [data, setData] = useState<{ parameters: any, results: number[][] } | null>(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isPlaying && data) {
      interval = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= data.results.length - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, 50); // 50ms per frame
    }
    return () => clearInterval(interval);
  }, [isPlaying, data]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/diffusion/numerical/?alpha=110&nx=50&time_steps=200');
      const json = await response.json();
      setData(json);
      setCurrentStep(0);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const currentTemperatures = data ? data.results[currentStep] : [];
  const rodLength = 15;
  const segmentLength = currentTemperatures.length > 0 ? rodLength / currentTemperatures.length : 1;

  return (
    <div className="simulation-container">
      <div className="canvas-wrapper">
        {loading && (
          <div className="loading-overlay">
            Loading simulation...
          </div>
        )}
        <Canvas camera={{ position: [0, 0, 15] }}>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} intensity={1} />
          <OrbitControls />
          
          {/* Group to rotate the rod to lay horizontally */}
          <group rotation={[0, 0, Math.PI / 2]}>
            {currentTemperatures.map((temp, index) => {
              const yPosition = (index - currentTemperatures.length / 2) * segmentLength + segmentLength / 2;
              return (
                <RodSegment 
                  key={index} 
                  position={[0, yPosition, 0]} 
                  color={getTemperatureColor(temp)} 
                  length={segmentLength} 
                />
              );
            })}
          </group>
        </Canvas>
      </div>

      {data && (
        <div className="controls-panel">
          <div className="controls-row">
            <button 
              onClick={() => setIsPlaying(!isPlaying)}
              className="control-btn primary-btn"
            >
              {isPlaying ? <Pause size={20} /> : <Play size={20} />}
            </button>
            <button 
              onClick={() => { setIsPlaying(false); setCurrentStep(0); }}
              className="control-btn secondary-btn"
            >
              <RotateCcw size={20} />
            </button>
            
            <div className="slider-wrapper">
              <input 
                type="range" 
                min="0" 
                max={data.results.length - 1} 
                value={currentStep}
                onChange={(e) => {
                  setIsPlaying(false);
                  setCurrentStep(parseInt(e.target.value));
                }}
                className="time-slider"
              />
              <span className="step-label">
                Time: {(currentStep * data.parameters.dt).toFixed(3)}s
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SimulationCanvas;
