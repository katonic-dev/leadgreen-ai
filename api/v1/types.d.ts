// Lead Green API v1 types, generated from the published documents on 2026-09-27 (data_version 2026-09-27).
// Additive only within v1: new optional fields may appear.

export type Manifest = {
  version: string;
  updated: string;
  data_version: string;
  site: string;
  name: string;
  description: string;
  endpoints: Array<{
    path: string;
    url: string;
    description: string;
  }>;
  sources: Array<unknown>;
  licence: string;
  caveat: string;
  boundary: string;
  publisher: {
    name: string;
    parent: string;
    url: string;
    entity: string;
    registration: string;
    jurisdiction: string;
    address: string | null;
    contact: string;
    response_working_days: number;
  };
  attribution: string;
  releases: {
    index: string;
    pattern: string;
  };
};

export type Index = {
  version: string;
  updated: string;
  data_version: string;
  unit: string;
  workload: string;
  itl_deadline_ms: number;
  selection: string;
  reference_row: {
    model: string;
    gpu: string;
    num_gpus: number;
  };
  source: Record<string, unknown>;
  caveat: string;
  boundary: string;
  rows: Array<{
    model: string;
    slug: string;
    model_id: string;
    params_b: number;
    active_params_b: number;
    precision: string;
    gpu: string;
    num_gpus: number;
    wh_per_million_output_tokens: number;
    joules_per_output_token: number;
    median_itl_ms: number;
    avg_requests_in_flight: number;
    gpu_power_watts_total: number;
    avg_output_tokens: number;
    avg_running_batch: number;
    max_num_seqs: number;
    row_id: string;
  }>;
};

export type Models = {
  version: string;
  updated: string;
  data_version: string;
  source: Record<string, unknown>;
  models: Array<{
    slug: string;
    name: string;
    model_id: string;
    params_b: number;
    active_params_b: number;
    gpus: Array<string>;
    url: string;
    page: string;
  }>;
};

export type Model = {
  version: string;
  updated: string;
  data_version: string;
  unit: string;
  itl_deadline_ms: number;
  source: Record<string, unknown>;
  caveat: string;
  boundary: string;
  slug: string;
  name: string;
  model_id: string;
  params_b: number;
  active_params_b: number;
  architecture: string;
  gpus: Array<string>;
  configurations: Array<{
    gpu: string;
    num_gpus: number;
    tensor_parallel: number;
    data_parallel: number;
    expert_parallel: number;
    precision: string;
    max_num_seqs: number;
    avg_requests_in_flight: number;
    wh_per_million_output_tokens: number;
    joules_per_output_token: number;
    median_itl_ms: number;
    p90_itl_ms: number;
    p99_itl_ms: number;
    tokens_per_second: number;
    gpu_power_watts_total: number;
    avg_output_tokens: number;
    under_itl_deadline: boolean;
    avg_running_batch: number;
    p95_itl_ms: number;
    row_id: string;
    repeat: number;
  }>;
  best: Record<string, {
    gpu: string;
    num_gpus: number;
    tensor_parallel: number;
    data_parallel: number;
    expert_parallel: number;
    precision: string;
    max_num_seqs: number;
    avg_requests_in_flight: number;
    wh_per_million_output_tokens: number;
    joules_per_output_token: number;
    median_itl_ms: number;
    p90_itl_ms: number;
    p99_itl_ms: number;
    tokens_per_second: number;
    gpu_power_watts_total: number;
    avg_output_tokens: number;
    under_itl_deadline: boolean;
    avg_running_batch: number;
    p95_itl_ms: number;
    row_id: string;
    repeat: number;
  }>;
};

export type Grid = {
  version: string;
  updated: string;
  data_version: string;
  year: string;
  unit: string;
  basis: string;
  source: Record<string, unknown>;
  licence: string;
  world: number;
  note: string;
  areas: Array<{
    iso3: string;
    name: string;
    area_type: string;
    g_co2e_per_kwh: number;
    display_name: string;
    iso2: null | string;
    years: Record<string, number>;
    latest_year: string;
    continent?: string;
  }>;
};

export type Hardware = {
  version: string;
  updated: string;
  data_version: string;
  retrieved: string;
  note: string;
  tdp: Array<{
    gpu: string;
    form: string;
    max_tdp_w: number;
    tdp_label: string;
    memory: string;
    source: string;
  }>;
  systems: Array<{
    system: string;
    gpus: string;
    max_power_kw: number;
    label: string;
    source: string;
  }>;
  mig_profiles: Array<{
    gpu: string;
    profile: string;
    memory_fraction: string;
    sm_fraction: string;
    instances: number;
  }>;
  embodied: {
    item: string;
    kg_co2e_cradle_to_gate: number;
    source: string;
    published: string;
  };
  sources: Array<unknown>;
};

export type PerQuery = {
  version: string;
  updated: string;
  data_version: string;
  unit: string;
  round: string;
  setup: string;
  classes: Record<string, string>;
  score: string;
  note: string;
  source: Record<string, unknown>;
  rows: Array<{
    model: string;
    class: string;
    wh_per_1000_queries: number;
    score: number;
    source_label: string;
    note?: string;
  }>;
};

export type Measurements = {
  version: string;
  updated: string;
  data_version: string;
  unit: string;
  protocol_version: string;
  schema: string;
  itl_deadline_ms: number;
  note: string;
  caveat: string;
  boundary: string;
  rows: Array<unknown>;
};

export type Changes = {
  version: string;
  updated: string;
  data_version: string;
  note: string;
  changes: Array<{
    date: string;
    summary: string;
    documents: Array<string>;
    reason: string;
    source_version: string;
  }>;
};
