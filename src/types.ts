export interface Topic {
  id: string;
  unit_number: number;
  name: string;
  description: string;
  icon: string;
  concept_count?: number;
  mastery?: number;
}

export interface UnitGroup {
  unit_number: number;
  title: string;
  topics: Topic[];
  total_concepts: number;
}

export interface Concept {
  id: string;
  topic_id: string;
  name: string;
  definition: string;
  explanation: string;
  simple_explanation: string;
  example: string;
  related_concepts?: string[];
  common_confusions?: string;
  difficulty: 'facil' | 'medio' | 'dificil' | 'experto';
  source_document: string;
  source_page: string;
  order_idx: number;
  user_mastery?: number;
  user_status?: 'no_estudiado' | 'en_progreso' | 'debil' | 'dominado';
  needs_practice_flag?: number;
  note_text?: string;
}

export interface QuestionOption {
  id?: string;
  text?: string;
  left?: string;
  right?: string;
}

export interface Question {
  id: string;
  topic_id: string;
  concept_id: string;
  concept_name?: string;
  type: 'multiple_choice' | 'true_false' | 'fill_blank' | 'matching' | 'order_steps' | 'open_question' | 'practical_case';
  difficulty: 'facil' | 'medio' | 'dificil' | 'experto';
  question: string;
  options?: any;
  has_hint1?: boolean;
  has_hint2?: boolean;
  source_document: string;
  source_page: string;
}

export interface GradedResult {
  score: number;
  is_correct: boolean;
  strengths: string[];
  missing: string[];
  confusions: string[];
  model_answer: string;
  tips: string;
}

export interface SubmitResponse {
  result: GradedResult;
  xp_earned: number;
  concept_progress: {
    concept_id: string;
    new_mastery: number;
    status: string;
    next_review: string;
  };
  explanation: string;
  source_citation: string;
}

export interface DashboardData {
  user: {
    id: string;
    name: string;
    email: string;
    xp: number;
    level: number;
    streak_days: number;
    study_time_seconds: number;
  };
  overall_progress_percent: number;
  stats: {
    total_concepts: number;
    dominados: number;
    en_progreso: number;
    debiles: number;
    no_estudiados: number;
    total_attempts: number;
    total_correct: number;
    accuracy_percent: number;
  };
  unit_progress: Array<{
    unit: number;
    mastery: number;
    concept_count: number;
  }>;
  continue_studying?: {
    id: string;
    name: string;
    topic_name: string;
    unit_number: number;
  };
  weak_topics: Array<{
    topic_name: string;
    weak_count: number;
  }>;
}

export interface CaseStudy {
  id: string;
  title: string;
  category: string;
  description: string;
  schema_ddl?: string;
  total_queries: number;
  sample_queries?: Array<{
    num: number;
    prompt: string;
    solution: string;
    explanation: string;
  }>;
  source_document: string;
}
