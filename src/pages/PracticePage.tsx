import React, { useState, useEffect } from 'react';
import {
  BrainCircuit,
  Lightbulb,
  HelpCircle,
  CheckCircle2,
  XCircle,
  ArrowRight,
  Sparkles,
  Zap,
  Filter,
  FileText,
  MessageSquare,
  ArrowUp,
  ArrowDown,
  RefreshCw
} from 'lucide-react';
import { Question, SubmitResponse } from '../types';
import { fetchNextQuestion, submitQuestionAnswer, fetchQuestionHint, explainDifferently } from '../api';
import MathText from '../components/MathText';

interface PracticePageProps {
  initialTopicId?: string;
  onRefreshDashboard?: () => void;
}

export const PracticePage: React.FC<PracticePageProps> = ({
  initialTopicId,
  onRefreshDashboard
}) => {
  // Question & Session state
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [loadingQuestion, setLoadingQuestion] = useState<boolean>(true);
  const [noMoreQuestions, setNoMoreQuestions] = useState<boolean>(false);

  // Filter state
  const [topicFilter, setTopicFilter] = useState<string>(initialTopicId || '');
  const [difficultyFilter, setDifficultyFilter] = useState<string>('');
  const [typeFilter, setTypeFilter] = useState<string>('');

  // User input state
  const [userAnswer, setUserAnswer] = useState<string>('');
  const [matchingPairs, setMatchingPairs] = useState<Record<string, string>>({});
  const [orderedItems, setOrderedItems] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [submissionResult, setSubmissionResult] = useState<SubmitResponse | null>(null);

  // Hints & Tutor state
  const [hint1, setHint1] = useState<string | null>(null);
  const [hint2, setHint2] = useState<string | null>(null);
  const [loadingHint, setLoadingHint] = useState<number | null>(null);
  const [tutorExplanation, setTutorExplanation] = useState<any | null>(null);
  const [showTutorModal, setShowTutorModal] = useState<boolean>(false);
  const [loadingTutor, setLoadingTutor] = useState<boolean>(false);

  // Timing
  const [startTime, setStartTime] = useState<number>(Date.now());

  // Load question
  const loadQuestion = async () => {
    try {
      setLoadingQuestion(true);
      setSubmissionResult(null);
      setUserAnswer('');
      setHint1(null);
      setHint2(null);
      setTutorExplanation(null);
      setShowTutorModal(false);
      setNoMoreQuestions(false);

      const q = await fetchNextQuestion({
        topicId: topicFilter || undefined,
        difficulty: difficultyFilter || undefined,
        qType: typeFilter || undefined
      });

      setCurrentQuestion(q);
      setStartTime(Date.now());

      // Prepare matching or order_steps state if applicable
      if (q.type === 'order_steps' && Array.isArray(q.options)) {
        // Shuffle initially
        const shuffled = [...q.options].sort(() => Math.random() - 0.5);
        setOrderedItems(shuffled);
      } else if (q.type === 'matching' && Array.isArray(q.options)) {
        setMatchingPairs({});
      }
    } catch (err: any) {
      console.warn('No more questions:', err);
      setNoMoreQuestions(true);
      setCurrentQuestion(null);
    } finally {
      setLoadingQuestion(false);
    }
  };

  useEffect(() => {
    loadQuestion();
  }, [topicFilter, difficultyFilter, typeFilter]);

  // Request Hint
  const handleRequestHint = async (hintNum: number) => {
    if (!currentQuestion) return;
    try {
      setLoadingHint(hintNum);
      const res = await fetchQuestionHint(currentQuestion.id, hintNum);
      if (hintNum === 1) setHint1(res.hint);
      if (hintNum === 2) setHint2(res.hint);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingHint(null);
    }
  };

  // Request "Explícame de otra manera"
  const handleExplainDifferently = async () => {
    if (!currentQuestion) return;
    try {
      setLoadingTutor(true);
      setShowTutorModal(true);
      const res = await explainDifferently(currentQuestion.concept_id);
      setTutorExplanation(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingTutor(false);
    }
  };

  // Move step up or down in order_steps
  const moveStep = (index: number, direction: 'up' | 'down') => {
    const newItems = [...orderedItems];
    const targetIndex = direction === 'up' ? index - 1 : index + 1;
    if (targetIndex < 0 || targetIndex >= newItems.length) return;
    const temp = newItems[index];
    newItems[index] = newItems[targetIndex];
    newItems[targetIndex] = temp;
    setOrderedItems(newItems);
  };

  // Submit answer
  const handleSubmit = async () => {
    if (!currentQuestion) return;

    let finalAnswer = userAnswer;

    if (currentQuestion.type === 'order_steps') {
      finalAnswer = JSON.stringify(orderedItems);
    } else if (currentQuestion.type === 'matching') {
      finalAnswer = JSON.stringify(matchingPairs);
    }

    if (!finalAnswer.trim()) return;

    try {
      setSubmitting(true);
      const timeSpent = Math.max(1, Math.round((Date.now() - startTime) / 1000));
      const res = await submitQuestionAnswer({
        questionId: currentQuestion.id,
        userAnswer: finalAnswer,
        timeSeconds: timeSpent
      });

      setSubmissionResult(res);
      if (onRefreshDashboard) onRefreshDashboard();
    } catch (err) {
      console.error('Error submitting answer', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header & Filter Controls */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-navy-900">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-black text-slate-900 dark:text-white flex items-center space-x-2">
              <BrainCircuit className="h-5 w-5 text-teal-600" />
              <span>Práctica Conceptual Adaptativa</span>
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Banco de preguntas calibrado con sistema anti-repetición y evaluación semántica.
            </p>
          </div>

          {/* Quick Filters */}
          <div className="flex flex-wrap items-center gap-2">
            <select
              value={difficultyFilter}
              onChange={(e) => setDifficultyFilter(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-700 min-h-[40px] dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
            >
              <option value="">Todas las dificultades</option>
              <option value="facil">Fácil</option>
              <option value="medio">Medio</option>
              <option value="dificil">Difícil</option>
              <option value="experto">Experto</option>
            </select>

            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-700 min-h-[40px] dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
            >
              <option value="">Todos los formatos</option>
              <option value="multiple_choice">Opción Múltiple</option>
              <option value="true_false">Verdadero / Falso</option>
              <option value="fill_blank">Completar Término</option>
              <option value="order_steps">Ordenar Pasos</option>
              <option value="open_question">Pregunta de Desarrollo</option>
            </select>

            <button
              onClick={loadQuestion}
              className="rounded-xl border border-slate-200 bg-slate-50 p-2.5 text-slate-600 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300 min-h-[40px] min-w-[40px] flex items-center justify-center"
              title="Cargar otra pregunta"
              aria-label="Cargar otra pregunta"
            >
              <RefreshCw className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Question Presentation Container */}
      {loadingQuestion ? (
        <div className="flex h-72 items-center justify-center rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-navy-900">
          <div className="text-center text-slate-500">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-teal-500 border-t-transparent mx-auto mb-3"></div>
            Seleccionando la pregunta óptima según tu historial...
          </div>
        </div>
      ) : noMoreQuestions ? (
        <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center dark:border-slate-800 dark:bg-navy-900 shadow-sm">
          <CheckCircle2 className="h-12 w-12 text-teal-600 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">
            ¡Felicitaciones! Has completado las preguntas disponibles con este filtro.
          </h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto mt-1 mb-5">
            El sistema anti-repetición ha agotado las preguntas pendientes en esta categoría. Podés resetear los filtros o practicar en el Simulador de Examen.
          </p>
          <button
            onClick={() => {
              setTopicFilter('');
              setDifficultyFilter('');
              setTypeFilter('');
            }}
            className="rounded-xl bg-teal-600 px-5 py-2.5 text-xs font-bold text-white hover:bg-teal-700"
          >
            Limpiar Filtros y Seguir Practicando
          </button>
        </div>
      ) : currentQuestion ? (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm dark:border-slate-800 dark:bg-navy-900 space-y-6">
          {/* Question Metadata Header */}
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4 dark:border-slate-800">
            <div className="flex items-center space-x-2">
              <span className="rounded-md bg-teal-50 px-2.5 py-1 text-xs font-bold text-teal-700 dark:bg-teal-950 dark:text-teal-400">
                {currentQuestion.concept_name || 'Concepto Clave'}
              </span>
              <span
                className={`rounded-md px-2 py-0.5 text-[11px] font-bold uppercase ${
                  currentQuestion.difficulty === 'facil'
                    ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-400'
                    : currentQuestion.difficulty === 'medio'
                    ? 'bg-blue-50 text-blue-700 dark:bg-blue-950 dark:text-blue-400'
                    : 'bg-amber-50 text-amber-700 dark:bg-amber-950 dark:text-amber-400'
                }`}
              >
                {currentQuestion.difficulty}
              </span>
            </div>

            <div className="flex items-center space-x-2">
              <span className="inline-flex items-center space-x-1 rounded-md bg-slate-100 px-2.5 py-1 text-[11px] font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                <FileText className="h-3 w-3 text-slate-400" />
                <span>{currentQuestion.source_document} (pág. {currentQuestion.source_page})</span>
              </span>
            </div>
          </div>

          {/* Question Statement */}
          <div className="text-base sm:text-lg font-bold text-slate-900 dark:text-white leading-snug">
            <MathText content={currentQuestion.question} />
          </div>

          {/* Interactive Input based on Question Type */}
          <div className="space-y-4 pt-2">
            {/* 1. Multiple Choice */}
            {currentQuestion.type === 'multiple_choice' && (
              <div className="grid grid-cols-1 gap-3">
                {Array.isArray(currentQuestion.options) &&
                  currentQuestion.options.map((opt: any, idx: number) => {
                    const optId = opt.id || String.fromCharCode(65 + idx);
                    const optText = opt.text || opt;
                    const isSelected = userAnswer === optId;

                    return (
                      <button
                        key={idx}
                        disabled={submitting || !!submissionResult}
                        onClick={() => setUserAnswer(optId)}
                        className={`flex items-start space-x-3 rounded-xl border p-4 text-left text-sm transition-all ${
                          isSelected
                            ? 'border-teal-500 bg-teal-50/70 font-semibold text-teal-900 dark:border-teal-500 dark:bg-teal-950/40 dark:text-teal-200 shadow-sm'
                            : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-slate-800 dark:border-slate-800 dark:text-slate-200 dark:hover:bg-slate-800/60'
                        }`}
                      >
                        <span
                          className={`flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-lg text-xs font-bold ${
                            isSelected
                              ? 'bg-teal-600 text-white'
                              : 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
                          }`}
                        >
                          {optId}
                        </span>
                        <div className="pt-0.5">
                          <MathText content={optText} />
                        </div>
                      </button>
                    );
                  })}
              </div>
            )}

            {/* 2. True / False */}
            {currentQuestion.type === 'true_false' && (
              <div className="grid grid-cols-2 gap-4">
                {['verdadero', 'falso'].map((val) => {
                  const isSelected = userAnswer.toLowerCase() === val;
                  return (
                    <button
                      key={val}
                      disabled={submitting || !!submissionResult}
                      onClick={() => setUserAnswer(val)}
                      className={`rounded-2xl border p-6 text-center font-bold capitalize transition-all ${
                        isSelected
                          ? val === 'verdadero'
                            ? 'border-emerald-500 bg-emerald-50 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300'
                            : 'border-rose-500 bg-rose-50 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300'
                          : 'border-slate-200 hover:bg-slate-50 text-slate-800 dark:border-slate-800 dark:text-slate-200 dark:hover:bg-slate-800'
                      }`}
                    >
                      <div className="text-lg">{val}</div>
                    </button>
                  );
                })}
              </div>
            )}

            {/* 3. Fill in the Blank */}
            {currentQuestion.type === 'fill_blank' && (
              <div className="space-y-2">
                <input
                  type="text"
                  disabled={submitting || !!submissionResult}
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="Escribí aquí el término exacto..."
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 p-3.5 text-sm text-slate-900 focus:border-teal-500 focus:outline-none dark:border-slate-700 dark:bg-slate-800 dark:text-white"
                />
              </div>
            )}

            {/* 4. Open Question / Desarrollo */}
            {currentQuestion.type === 'open_question' && (
              <div className="space-y-2">
                <div className="text-xs text-slate-500 mb-1">
                  Redactá tu respuesta con tus propias palabras. El corrector semántico evaluará tus puntos fuertes, omisiones y conceptos clave:
                </div>
                <textarea
                  rows={4}
                  disabled={submitting || !!submissionResult}
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="Escribí aquí tu explicación técnica completa..."
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 p-3.5 text-sm text-slate-900 focus:border-teal-500 focus:outline-none dark:border-slate-700 dark:bg-slate-800 dark:text-white"
                />
                <div className="text-right text-[11px] text-slate-400">
                  {userAnswer.length} caracteres
                </div>
              </div>
            )}

            {/* 5. Order Steps */}
            {currentQuestion.type === 'order_steps' && (
              <div className="space-y-2">
                <div className="text-xs text-slate-500 mb-2">
                  Organizá los pasos en la secuencia cronológica correcta usando las flechas:
                </div>
                {orderedItems.map((item, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 p-3 text-xs dark:border-slate-700 dark:bg-slate-800/60"
                  >
                    <div className="flex items-center space-x-3">
                      <span className="flex h-5 w-5 items-center justify-center rounded-full bg-slate-200 dark:bg-slate-700 text-[11px] font-bold">
                        {idx + 1}
                      </span>
                      <span className="text-slate-800 dark:text-slate-200 font-medium">
                        <MathText content={item} />
                      </span>
                    </div>
                    {!submissionResult && (
                      <div className="flex items-center space-x-1">
                        <button
                          disabled={idx === 0}
                          onClick={() => moveStep(idx, 'up')}
                          className="rounded p-1 hover:bg-slate-200 disabled:opacity-30 dark:hover:bg-slate-700"
                        >
                          <ArrowUp className="h-3.5 w-3.5" />
                        </button>
                        <button
                          disabled={idx === orderedItems.length - 1}
                          onClick={() => moveStep(idx, 'down')}
                          className="rounded p-1 hover:bg-slate-200 disabled:opacity-30 dark:hover:bg-slate-700"
                        >
                          <ArrowDown className="h-3.5 w-3.5" />
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Progressive Hints & Explícame de otra manera toolbar */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-t border-slate-100 pt-4 dark:border-slate-800">
            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={() => handleRequestHint(1)}
                className="inline-flex items-center space-x-1.5 rounded-xl border border-amber-300 bg-amber-50 px-3 py-2 text-xs font-bold text-amber-800 hover:bg-amber-100 active:scale-98 min-h-[40px] dark:border-amber-900/60 dark:bg-amber-950/40 dark:text-amber-300"
              >
                <Lightbulb className="h-4 w-4 text-amber-600" />
                <span>Pista 1</span>
              </button>

              <button
                onClick={() => handleRequestHint(2)}
                className="inline-flex items-center space-x-1.5 rounded-xl border border-amber-300 bg-amber-50 px-3 py-2 text-xs font-bold text-amber-800 hover:bg-amber-100 active:scale-98 min-h-[40px] dark:border-amber-900/60 dark:bg-amber-950/40 dark:text-amber-300"
              >
                <Lightbulb className="h-4 w-4 text-amber-600" />
                <span>Pista 2</span>
              </button>

              <button
                onClick={handleExplainDifferently}
                className="inline-flex items-center space-x-1.5 rounded-xl border border-indigo-200 bg-indigo-50 px-3 py-2 text-xs font-bold text-indigo-700 hover:bg-indigo-100 active:scale-98 min-h-[40px] dark:border-indigo-900/60 dark:bg-indigo-950/40 dark:text-indigo-300"
              >
                <HelpCircle className="h-4 w-4 text-indigo-600" />
                <span>Explicación alternativa</span>
              </button>
            </div>

            {/* Action Buttons */}
            <div>
              {!submissionResult ? (
                <button
                  disabled={submitting}
                  onClick={handleSubmit}
                  className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 rounded-xl bg-teal-600 px-6 py-2.5 text-xs font-bold text-white shadow-md hover:bg-teal-700 active:scale-98 min-h-[42px] disabled:opacity-50"
                >
                  {submitting ? (
                    <span>Evaluando respuesta...</span>
                  ) : (
                    <>
                      <Sparkles className="h-4 w-4" />
                      <span>Comprobar Respuesta</span>
                    </>
                  )}
                </button>
              ) : (
                <button
                  onClick={loadQuestion}
                  className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 rounded-xl bg-teal-600 px-6 py-2.5 text-xs font-bold text-white shadow-md hover:bg-teal-700 active:scale-98 min-h-[42px]"
                >
                  <span>Siguiente Pregunta</span>
                  <ArrowRight className="h-4 w-4" />
                </button>
              )}
            </div>
          </div>

          {/* Unfolded Hints */}
          {hint1 && (
            <div className="rounded-xl border border-amber-200 bg-amber-50/80 p-3 text-xs text-amber-900 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-300">
              <strong className="font-bold">💡 Pista 1: </strong>
              <MathText content={hint1} />
            </div>
          )}
          {hint2 && (
            <div className="rounded-xl border border-amber-200 bg-amber-50/80 p-3 text-xs text-amber-900 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-300">
              <strong className="font-bold">💡 Pista 2: </strong>
              <MathText content={hint2} />
            </div>
          )}

          {/* Submission Result Feedback Card */}
          {submissionResult && (
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 dark:border-slate-800 dark:bg-slate-800/50 space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 pb-3 dark:border-slate-700">
                <div className="flex items-center space-x-2">
                  {submissionResult.result.is_correct ? (
                    <div className="flex items-center space-x-1.5 text-emerald-600 font-bold text-base">
                      <CheckCircle2 className="h-5 w-5" />
                      <span>¡Respuesta Correcta! ({submissionResult.result.score}%)</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-1.5 text-rose-600 font-bold text-base">
                      <XCircle className="h-5 w-5" />
                      <span>Respuesta Parcial o Incorrecta ({submissionResult.result.score}%)</span>
                    </div>
                  )}
                </div>

                <div className="flex items-center space-x-3 text-xs">
                  <span className="flex items-center space-x-1 font-bold text-amber-600">
                    <Zap className="h-3.5 w-3.5 fill-amber-500" />
                    <span>+{submissionResult.xp_earned} XP</span>
                  </span>
                  <span className="font-medium text-slate-500">
                    Nuevo Dominio: {Math.round(submissionResult.concept_progress.new_mastery)}%
                  </span>
                </div>
              </div>

              {/* Semantic Feedback for Open Questions or Complex evaluations */}
              {submissionResult.result.strengths && submissionResult.result.strengths.length > 0 && (
                <div className="text-xs text-emerald-700 dark:text-emerald-400">
                  <div className="font-bold mb-1">✓ Puntos fuertes identificados en tu respuesta:</div>
                  <ul className="list-disc pl-5 space-y-0.5">
                    {submissionResult.result.strengths.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
              )}

              {submissionResult.result.missing && submissionResult.result.missing.length > 0 && (
                <div className="text-xs text-amber-700 dark:text-amber-400">
                  <div className="font-bold mb-1">⚠ Conceptos u omisiones a considerar:</div>
                  <ul className="list-disc pl-5 space-y-0.5">
                    {submissionResult.result.missing.map((m, i) => (
                      <li key={i}>{m}</li>
                    ))}
                  </ul>
                </div>
              )}

              {submissionResult.result.confusions && submissionResult.result.confusions.length > 0 && (
                <div className="text-xs text-rose-700 dark:text-rose-400">
                  <div className="font-bold mb-1">✗ Confusiones conceptuales detectadas:</div>
                  <ul className="list-disc pl-5 space-y-0.5">
                    {submissionResult.result.confusions.map((c, i) => (
                      <li key={i}>{c}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Model Answer */}
              {submissionResult.result.model_answer && (
                <div className="rounded-xl bg-white p-4 text-xs dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                  <div className="font-bold text-slate-800 dark:text-slate-200 mb-1">
                    Respuesta de Referencia / Explicación Oficial:
                  </div>
                  <div className="text-slate-600 dark:text-slate-300">
                    <MathText content={submissionResult.result.model_answer} />
                  </div>
                </div>
              )}

              {/* Official Citation */}
              <div className="text-[11px] text-slate-400">
                Alineado a: <span className="font-semibold text-slate-600 dark:text-slate-300">{submissionResult.source_citation}</span>
              </div>
            </div>
          )}
        </div>
      ) : null}

      {/* "Explícame de otra manera" Modal */}
      {showTutorModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm">
          <div className="max-w-xl w-full rounded-2xl bg-white p-6 shadow-2xl dark:bg-navy-900 border border-slate-200 dark:border-slate-800 max-h-[85vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3 dark:border-slate-800">
              <div className="flex items-center space-x-2">
                <Sparkles className="h-5 w-5 text-indigo-600" />
                <h3 className="font-bold text-slate-900 dark:text-white">
                  Tutor Didáctico: Explicación Alternativa
                </h3>
              </div>
              <button
                onClick={() => setShowTutorModal(false)}
                className="text-slate-400 hover:text-slate-600 text-sm font-bold"
              >
                ✕
              </button>
            </div>

            {loadingTutor ? (
              <div className="py-12 text-center text-xs text-slate-500">
                Generando analogías y casos de uso prácticos...
              </div>
            ) : tutorExplanation ? (
              <div className="mt-4 space-y-4 text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
                <div>
                  <h4 className="font-bold text-slate-900 dark:text-white text-sm">
                    {tutorExplanation.concept_name}
                  </h4>
                  <p className="mt-1">{tutorExplanation.simplified}</p>
                </div>

                <div className="rounded-xl bg-indigo-50/70 p-3.5 border border-indigo-100 dark:bg-indigo-950/30 dark:border-indigo-900">
                  <div className="font-bold text-indigo-900 dark:text-indigo-300 mb-1">
                    🌟 Analogía con la vida real:
                  </div>
                  <div>{tutorExplanation.analogy}</div>
                </div>

                <div className="rounded-xl bg-slate-50 p-3.5 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                  <div className="font-bold text-slate-900 dark:text-white mb-1">
                    💼 Caso empresarial concreto:
                  </div>
                  <div>{tutorExplanation.business_case}</div>
                </div>

                <div className="text-right pt-2">
                  <button
                    onClick={() => setShowTutorModal(false)}
                    className="rounded-xl bg-teal-600 px-4 py-2 text-xs font-bold text-white hover:bg-teal-700"
                  >
                    ¡Entendido! Volver a responder
                  </button>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
};

export default PracticePage;
