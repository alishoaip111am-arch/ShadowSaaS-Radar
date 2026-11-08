import { useState } from 'react'
import './App.css'

type Result = {
  user?: string
  app?: string
  score?: number
  level?: string
  evidence?: string[]
  assumptions?: string[]
  [key: string]: any
}

export default function App() {
  const [mode, setMode] = useState('shadow')
  const [source, setSource] = useState('generic')
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [data, setData] = useState<any>(null)

  async function analyze() {
    if (!file) {
      setError('Please select a CSV file first.')
      return
    }

    setLoading(true)
    setError('')
    setData(null)

    const form = new FormData()
    form.append('file', file)

    const endpoint = mode === 'shadow'
      ? '/api/analyze/shadow-ai'
      : '/api/analyze/iam'

    if (mode === 'shadow') {
      form.append('source', source)
    }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: form,
      })

      const result = await response.json()

      if (!response.ok) {
        throw new Error(result.detail || 'Analysis failed')
      }

      setData(result)
    } catch (err: any) {
      setError(err.message || 'Connection error')
    } finally {
      setLoading(false)
    }
  }

  const results: Result[] = data?.results || []
  const analysis = data?.analysis || {}

  return (
    <main className="dashboard">
      <header className="topbar">
        <div className="brand">
          <span className="brand-icon">S</span>
          <div>
            <h1>ShadowSaaS Radar</h1>
            <p>Identity Security · Shadow AI Detection</p>
          </div>
        </div>
        <span className="status">API Connected</span>
      </header>

      <section className="hero">
        <p className="eyebrow">SECURITY ANALYTICS PLATFORM</p>
        <h2>Visibility starts with identity.</h2>
        <p>
          Analyze authentication logs and identify patterns
          that may require security review.
        </p>
      </section>

      <section className="workspace">
        <div className="panel">
          <h3>Analysis Workspace</h3>

          <div className="tabs">
            <button
              className={mode === 'shadow' ? 'active' : ''}
              onClick={() => { setMode('shadow'); setData(null) }}
            >
              Shadow AI
            </button>
            <button
              className={mode === 'iam' ? 'active' : ''}
              onClick={() => { setMode('iam'); setData(null) }}
            >
              IAM Behavioral
            </button>
          </div>

          {mode === 'shadow' && (
            <label className="field">
              Log source
              <select value={source} onChange={e => setSource(e.target.value)}>
                <option value="hennge">HENNGE Access Logs</option>
                <option value="generic">Generic SSO CSV</option>
              </select>
            </label>
          )}

          <label className="upload">
            <span className="upload-icon">↑</span>
            <strong>{file ? file.name : 'Select a CSV file'}</strong>
            <small>Choose an authentication log file</small>
            <input
              type="file"
              accept=".csv"
              onChange={e => setFile(e.target.files?.[0] || null)}
            />
          </label>

          <button className="analyze" onClick={analyze} disabled={loading}>
            {loading ? 'Analyzing...' : 'Run Security Analysis'}
          </button>

          {error && <p className="error">{error}</p>}
        </div>

        {data && (
          <section className="results">
            <h3>Analysis Results</h3>

            {mode === 'shadow' ? (
              <>
                <div className="metrics">
                  <div><small>Events loaded</small><strong>{data.events_loaded}</strong></div>
                  <div><small>AI sign-in records</small><strong>{data.ai_usages_detected}</strong></div>
                  <div><small>Findings</small><strong>{data.results_count}</strong></div>
                </div>

                <h4>Risk Findings</h4>
                {results.length === 0 && <p>No AI usage patterns detected.</p>}

                {results.map((item, index) => (
                  <article className="finding" key={index}>
                    <div className="finding-head">
                      <strong>{item.user} → {item.app}</strong>
                      <span className={(item.level || '').toLowerCase()}>
                        {item.level || 'UNRATED'}
                      </span>
                    </div>
                    <strong className="score">{item.score}/100</strong>
                    <p>{Array.isArray(item.evidence)
                      ? item.evidence.join(' · ')
                      : String(item.evidence || '')}</p>
                    {Array.isArray(item.assumptions) && (
                      <small>{item.assumptions.join(' · ')}</small>
                    )}
                  </article>
                ))}

                <h4>Analysis Report</h4>
                <pre>{data.report}</pre>
                <p className="notice">{data.limitation}</p>
              </>
            ) : (
              <>
                <div className="metrics">
                  <div><small>Events scanned</small><strong>{analysis.events_scanned}</strong></div>
                  <div><small>Users analyzed</small><strong>{analysis.users_analyzed}</strong></div>
                  <div><small>Alerts</small><strong>{analysis.alerts?.length ?? 0}</strong></div>
                </div>

                <h4>Behavioral Alerts</h4>
                {(analysis.alerts || []).map((alert: any, index: number) => (
                  <article className="finding" key={index}>
                    <div className="finding-head">
                      <strong>{alert.user}</strong>
                      <span className={(alert.severity || '').toLowerCase()}>
                        {alert.severity}
                      </span>
                    </div>
                    <p>{alert.reason}</p>
                    <small>
                      Events: {alert.event_count} · Duration: {alert.duration_minutes} min
                    </small>
                  </article>
                ))}
                <p className="notice">{data.dataset_note}</p>
              </>
            )}
          </section>
        )}
      </section>

      <footer>
        ShadowSaaS Radar · Independent research prototype ·
        Based on authentication events only. These records do not establish AI prompt activity, file uploads or downloads, data transfers, data exfiltration, policy violations, or account compromise.
      </footer>
    </main>
  )
}
