"use client";

import {
  Activity,
  BadgeCheck,
  Clapperboard,
  Gauge,
  Loader2,
  RefreshCw,
  Scissors,
  Send,
  Sparkles,
} from "lucide-react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { FormEvent, useMemo, useState } from "react";
import type { AgentResult, RetentionPoint, ScreenTestResponse, Scene } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_AGENT_API_URL;

const samplePitch =
  "ScreenTest Studio helps seed-stage founders turn a messy product pitch into a short-form video plan, test it against synthetic target customers, and fix the weakest scene before filming.";

function retentionValue(point: RetentionPoint): number {
  return point.retention_pct ?? point.retention ?? 0;
}

function timeLabel(point: RetentionPoint, index: number): string {
  return point.time ?? `Scene ${index + 1}`;
}

function chartData(result?: AgentResult | null) {
  const before = result?.original_retention_curve ?? [];
  const after = result?.improved_retention_curve ?? [];
  const length = Math.max(before.length, after.length);

  return Array.from({ length }, (_, index) => ({
    time: timeLabel(before[index] ?? after[index] ?? {}, index),
    before: before[index] ? retentionValue(before[index]) : undefined,
    after: after[index] ? retentionValue(after[index]) : undefined,
  }));
}

function sceneTitle(scene: Scene) {
  return scene.text || scene.vo || scene.visual || "Untitled scene";
}

export default function Home() {
  const [brandPitch, setBrandPitch] = useState(samplePitch);
  const [brandUrl, setBrandUrl] = useState("");
  const [response, setResponse] = useState<ScreenTestResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const result = response?.result;
  const data = useMemo(() => chartData(result), [result]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    if (!API_URL) {
      setError("Set NEXT_PUBLIC_AGENT_API_URL to your TrueFoundry service URL.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_URL.replace(/\/$/, "")}/screen-tests`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          brand_pitch: brandPitch,
          brand_url: brandUrl.trim() || null,
        }),
      });

      const payload = await res.json();
      if (!res.ok) {
        throw new Error(payload.detail || "The agent service rejected the request.");
      }

      setResponse(payload);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand-mark">
          <Clapperboard size={24} />
          <span>ScreenTest Studio</span>
        </div>
        <div className="status-pill">
          <BadgeCheck size={17} />
          CrewAI on TrueFoundry, UI on Vercel
        </div>
      </header>

      <div className="main-grid">
        <form className="panel input-panel" onSubmit={submit}>
          <h1>Pre-screen a Reel before filming</h1>
          <p>
            The crew builds a timeline, runs a synthetic audience panel, diagnoses
            the drop-off, and rewrites the weakest scene.
          </p>

          <div className="field">
            <label htmlFor="brandPitch">Brand pitch</label>
            <textarea
              id="brandPitch"
              value={brandPitch}
              onChange={(event) => setBrandPitch(event.target.value)}
              minLength={20}
              required
            />
          </div>

          <div className="field">
            <label htmlFor="brandUrl">Brand URL</label>
            <input
              id="brandUrl"
              type="url"
              placeholder="https://example.com"
              value={brandUrl}
              onChange={(event) => setBrandUrl(event.target.value)}
            />
          </div>

          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? <Loader2 className="spin" size={18} /> : <Send size={18} />}
            {loading ? "Agents running" : "Run ScreenTest"}
          </button>
          <button
            className="secondary-button"
            type="button"
            onClick={() => setBrandPitch(samplePitch)}
          >
            <RefreshCw size={17} />
            Reset pitch
          </button>

          {error ? <div className="error">{error}</div> : null}
        </form>

        <section className="results">
          {!response ? (
            <div className="panel empty-state">
              <div>
                <Sparkles size={38} />
                <h2>Ready for the agent run</h2>
                <p>
                  Submit a startup pitch and the production CrewAI API will return
                  timeline cards, retention curves, a diagnosis, and a surgical rewrite.
                </p>
              </div>
            </div>
          ) : (
            <>
              <div className="summary-strip">
                <div className="panel metric">
                  <span>Run</span>
                  <strong>{response.status}</strong>
                </div>
                <div className="panel metric">
                  <span>Elapsed</span>
                  <strong>{response.elapsed_seconds}s</strong>
                </div>
                <div className="panel metric">
                  <span>Lift</span>
                  <strong>{result?.lift_metric ?? "Pending"}</strong>
                </div>
              </div>

              <div className="panel wide-panel">
                <div className="section-head">
                  <div>
                    <div className="icon-label">
                      <Gauge size={18} />
                      Retention curve
                    </div>
                    <p>Original vs. rewritten timeline</p>
                  </div>
                </div>
                <div className="chart-wrap">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                      <CartesianGrid stroke="#e6e0d6" />
                      <XAxis dataKey="time" />
                      <YAxis domain={[0, 100]} />
                      <Tooltip />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey="before"
                        name="Original"
                        stroke="#c4553d"
                        strokeWidth={3}
                        dot={{ r: 4 }}
                      />
                      <Line
                        type="monotone"
                        dataKey="after"
                        name="Rewritten"
                        stroke="#0f766e"
                        strokeWidth={3}
                        dot={{ r: 4 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {result?.founder_summary ? (
                <div className="panel wide-panel">
                  <div className="icon-label">
                    <Activity size={18} />
                    Founder summary
                  </div>
                  <p>{result.founder_summary}</p>
                </div>
              ) : null}

              <div className="panel wide-panel">
                <div className="section-head">
                  <div>
                    <div className="icon-label">
                      <Scissors size={18} />
                      Scene rewrite
                    </div>
                    <p>{result?.fix_rationale ?? "Waiting for parsed JSON output."}</p>
                  </div>
                </div>
                <div className="compare-grid">
                  <ScenePanel title="Original" scene={result?.original_scene} />
                  <ScenePanel title="Rewritten" scene={result?.rewritten_scene} />
                </div>
              </div>

              <div className="panel wide-panel">
                <div className="section-head">
                  <div>
                    <div className="icon-label">
                      <Clapperboard size={18} />
                      Updated timeline
                    </div>
                  </div>
                </div>
                <div className="scene-grid">
                  {(result?.updated_timeline ?? result?.original_timeline ?? []).map(
                    (scene, index) => (
                      <article className="panel scene-card" key={scene.scene_id ?? index}>
                        <div className="scene-meta">
                          <span>Scene {scene.scene_id ?? index + 1}</span>
                          <span>{scene.time_range}</span>
                        </div>
                        <h3>{sceneTitle(scene)}</h3>
                        <p>{scene.visual}</p>
                        {scene.vo ? <p>VO: {scene.vo}</p> : null}
                        {scene.sfx ? <p>SFX: {scene.sfx}</p> : null}
                      </article>
                    )
                  )}
                </div>
              </div>

              {!result ? (
                <pre className="json-panel">{response.raw_output}</pre>
              ) : null}
            </>
          )}
        </section>
      </div>
    </main>
  );
}

function ScenePanel({ title, scene }: { title: string; scene?: Scene }) {
  return (
    <article className="panel scene-card">
      <div className="scene-meta">
        <span>{title}</span>
        <span>{scene?.time_range}</span>
      </div>
      <h3>{scene ? sceneTitle(scene) : "No parsed scene"}</h3>
      <p>{scene?.visual}</p>
      {scene?.vo ? <p>VO: {scene.vo}</p> : null}
      {scene?.sfx ? <p>SFX: {scene.sfx}</p> : null}
    </article>
  );
}
