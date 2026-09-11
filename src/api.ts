import { DashboardData, UnitGroup, Topic, Concept, Question, SubmitResponse, CaseStudy } from './types';

const API_BASE = '/api';

export async function fetchDashboard(userId = 'default_user'): Promise<DashboardData> {
  const res = await fetch(`${API_BASE}/dashboard?user_id=${userId}`);
  if (!res.ok) throw new Error('Error al cargar dashboard');
  return res.json();
}

export async function fetchUnits(userId = 'default_user'): Promise<UnitGroup[]> {
  const res = await fetch(`${API_BASE}/theory/units?user_id=${userId}`);
  if (!res.ok) throw new Error('Error al cargar unidades');
  return res.json();
}

export async function fetchTopicDetail(topicId: string, userId = 'default_user'): Promise<Topic & { concepts: Concept[] }> {
  const res = await fetch(`${API_BASE}/theory/topics/${topicId}?user_id=${userId}`);
  if (!res.ok) throw new Error('Error al cargar tema');
  return res.json();
}

export async function setConceptFeedback(conceptId: string, action: 'entendido' | 'practicar', userId = 'default_user') {
  const res = await fetch(`${API_BASE}/theory/concept/${conceptId}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, action })
  });
  return res.json();
}

export async function saveConceptNote(conceptId: string, noteText: string, userId = 'default_user') {
  const res = await fetch(`${API_BASE}/theory/concept/${conceptId}/note`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, note_text: noteText })
  });
  return res.json();
}

export async function fetchNextQuestion(filters: {
  userId?: string;
  topicId?: string;
  difficulty?: string;
  qType?: string;
} = {}): Promise<Question> {
  const params = new URLSearchParams();
  if (filters.userId) params.append('user_id', filters.userId);
  if (filters.topicId) params.append('topic_id', filters.topicId);
  if (filters.difficulty) params.append('difficulty', filters.difficulty);
  if (filters.qType) params.append('q_type', filters.qType);

  const res = await fetch(`${API_BASE}/practice/next?${params.toString()}`);
  if (!res.ok) throw new Error('No hay más preguntas disponibles para este criterio');
  return res.json();
}

export async function submitQuestionAnswer(data: {
  userId?: string;
  questionId: string;
  userAnswer: string;
  timeSeconds?: number;
  attemptType?: string;
}): Promise<SubmitResponse> {
  const res = await fetch(`${API_BASE}/practice/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: data.userId || 'default_user',
      question_id: data.questionId,
      user_answer: data.userAnswer,
      time_seconds: data.timeSeconds || 0,
      attempt_type: data.attemptType || 'practice'
    })
  });
  if (!res.ok) {
    const errorBody = await res.text().catch(() => '');
    console.error('Error in /practice/submit:', res.status, errorBody);
    throw new Error(`Error al enviar respuesta (${res.status}): ${errorBody || res.statusText}`);
  }
  return res.json();
}

export async function fetchQuestionHint(questionId: string, hintNum: number): Promise<{ hint: string }> {
  const res = await fetch(`${API_BASE}/practice/hint/${questionId}/${hintNum}`);
  return res.json();
}

export async function explainDifferently(conceptId: string) {
  const res = await fetch(`${API_BASE}/practice/explain-differently/${conceptId}`);
  return res.json();
}

export async function fetchCases(): Promise<CaseStudy[]> {
  const res = await fetch(`${API_BASE}/cases`);
  return res.json();
}

export async function fetchCaseDetail(caseId: string): Promise<CaseStudy> {
  const res = await fetch(`${API_BASE}/cases/${caseId}`);
  return res.json();
}

export async function startExam(config: {
  userId?: string;
  numQuestions?: number;
  durationMinutes?: number;
  topicIds?: string[];
}) {
  const res = await fetch(`${API_BASE}/exam/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: config.userId || 'default_user',
      num_questions: config.numQuestions || 15,
      duration_minutes: config.durationMinutes || 45,
      topic_ids: config.topicIds
    })
  });
  if (!res.ok) throw new Error('Error al iniciar simulacro');
  return res.json();
}

export async function submitExam(sessionId: string, answers: Record<string, string>, timeSpentSeconds: number, userId = 'default_user') {
  const res = await fetch(`${API_BASE}/exam/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      user_id: userId,
      answers,
      time_spent_seconds: timeSpentSeconds
    })
  });
  if (!res.ok) throw new Error('Error al entregar simulacro');
  return res.json();
}

export async function fetchErrors(userId = 'default_user') {
  const res = await fetch(`${API_BASE}/errors?user_id=${userId}`);
  return res.json();
}

export async function resetErrors(mode: 'errors' | 'all' = 'errors', userId = 'default_user') {
  const res = await fetch(`${API_BASE}/errors/reset`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, mode })
  });
  if (!res.ok) throw new Error('Error al resetear errores');
  return res.json();
}

export async function searchKnowledge(query: string) {
  const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
  return res.json();
}

export async function fetchAdminStats() {
  const res = await fetch(`${API_BASE}/admin/stats`);
  return res.json();
}

export async function fetchAdminDocuments() {
  const res = await fetch(`${API_BASE}/admin/documents`);
  return res.json();
}

export async function fetchAdminQuestions(params: { topicId?: string; qType?: string; difficulty?: string } = {}) {
  const query = new URLSearchParams();
  if (params.topicId) query.append('topic_id', params.topicId);
  if (params.qType) query.append('q_type', params.qType);
  if (params.difficulty) query.append('difficulty', params.difficulty);
  const res = await fetch(`${API_BASE}/admin/questions?${query.toString()}`);
  return res.json();
}

export async function deleteAdminQuestion(qId: string) {
  const res = await fetch(`${API_BASE}/admin/questions/${qId}`, { method: 'DELETE' });
  return res.json();
}
