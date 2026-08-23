import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = import.meta.env.VITE_API_URL || "";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);

  const analyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/analyze`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({symptoms_text: text, include_llm: true})
      });
      if (!res.ok) throw new Error("Analysis failed");
      setResult(await res.json());
    } catch (e) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    const res = await fetch(`${API}/api/report`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({symptoms_text: text, include_llm: true})
    });
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "clinical_ai_report.pdf";
    a.click();
    URL.revokeObjectURL(url);
  };

  const startVoice = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition is not supported by this browser.");
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.onstart = () => setListening(true);
    recognition.onend = () => setListening(false);
    recognition.onresult = e => setText(prev => `${prev} ${e.results[0][0].transcript}`.trim());
    recognition.start();
  };

  return (
    <main className="page">
      <header className="hero">
        <div>
          <span className="badge">Healthcare AI • NLP + ML</span>
          <h1>Clinical Decision Support AI</h1>
          <p>Describe symptoms in natural language and receive an educational, model-assisted assessment.</p>
        </div>
        <div className="shield">AI</div>
      </header>

      <section className="card">
        <label htmlFor="symptoms">Describe your symptoms</label>
        <textarea id="symptoms" value={text} onChange={e => setText(e.target.value)}
          placeholder="Example: I have fever, cough, sore throat and fatigue for two days..." />
        <div className="actions">
          <button className="secondary" onClick={startVoice}>{listening ? "Listening…" : "🎙 Voice Input"}</button>
          <button onClick={analyze} disabled={loading}>{loading ? "Analyzing…" : "Analyze Symptoms"}</button>
        </div>
        <p className="hint">Do not enter personally identifiable information.</p>
      </section>

      {result && (
        <section className="results">
          <div className={`severity ${result.severity}`}>
            <strong>Severity: {result.severity.toUpperCase()}</strong>
            <span>Educational risk classification</span>
          </div>

          {result.red_flags.length > 0 && (
            <div className="alert">
              <strong>Safety notice</strong>
              {result.red_flags.map((x, i) => <p key={i}>{x}</p>)}
            </div>
          )}

          <div className="grid">
            <div className="card">
              <h2>Extracted Symptoms</h2>
              <div className="chips">
                {result.extracted_symptoms.length
                  ? result.extracted_symptoms.map(s => <span key={s}>{s}</span>)
                  : <span>No supported symptom terms detected</span>}
              </div>
            </div>

            <div className="card">
              <h2>Top Predictions</h2>
              {result.predictions.map(p => (
                <div className="prediction" key={p.disease}>
                  <div><b>{p.disease}</b><span>{(p.confidence * 100).toFixed(1)}%</span></div>
                  <div className="bar"><i style={{width: `${Math.min(100, p.confidence * 100)}%`}} /></div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h2>Educational Guidance</h2>
            <p className="advice">{result.advice}</p>
            <button onClick={downloadReport}>Download PDF Report</button>
          </div>

          <div className="disclaimer">{result.disclaimer}</div>
        </section>
      )}

      <footer>Prototype for educational and engineering demonstration • Human clinical oversight required</footer>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
