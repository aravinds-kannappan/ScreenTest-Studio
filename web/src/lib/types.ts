export type RetentionPoint = {
  time?: string;
  retention_pct?: number;
  retention?: number;
};

export type Scene = {
  scene_id?: number;
  time_range?: string;
  visual?: string;
  text?: string | null;
  vo?: string | null;
  sfx?: string | null;
  music_energy?: string;
};

export type AgentResult = {
  brand_profile?: Record<string, unknown>;
  original_timeline?: Scene[];
  updated_timeline?: Scene[];
  personas?: Array<Record<string, unknown>>;
  original_retention_curve?: RetentionPoint[];
  improved_retention_curve?: RetentionPoint[];
  diagnosis?: Record<string, unknown>;
  original_scene?: Scene;
  rewritten_scene?: Scene;
  lift_metric?: string;
  fix_rationale?: string;
  founder_summary?: string;
};

export type ScreenTestResponse = {
  run_id: string;
  status: string;
  elapsed_seconds: number;
  result: AgentResult | null;
  raw_output: string;
};
