import React, { useState, useEffect } from 'react';
import {
  GraduationCap,
  Clock,
  CheckCircle,
  XCircle,
  AlertTriangle,
  ArrowRight,
  ArrowLeft,
  RotateCcw,
  Sparkles,
  FileText,
  HelpCircle,
  BrainCircuit
} from 'lucide-react';
import { startExam, submitExam } from '../api';
import MathText from '../components/MathText';

interface ExamPageProps {
  onNavigateToPractice: (topicId?: string) => void;
  onRefreshDashboard?: () => void;
}

export const ExamPage: React.FC<ExamPageProps> = ({
  onNavigateToPractice,
  onRefreshDashboard
}) => {
  // Setup state
  const [numQuestions, setNumQuestions] = useState<number>(15);
  const [durationMinutes, setDurationMinutes] = useState<number>(30);
  const [examStatus, setExamStatus] = useState<'setup' | 'active' | 'results'>('setup');
  const [loading, setLoading] = useState<boolean>(false);

  // Active Exam state
  const [sessionId, setSessionId] = useState<string>('');
  const [examQuestions, setExamQuestions] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [userAnswers, setUserAnswers] = useState<Record<string, string>>({});
  const [secondsRemaining, setSecondsRemaining] = useState<number>(0);
  const [timeSpentSeconds, setTimeSpentSeconds] = useState<number>(0);

  // Results state
  const [examResults, setExamResults] = useState<any | null>(null);

  // Timer effect during active exam
  useEffect(() => {
    if (examStatus !== 'active' || secondsRemaining <= 0) return;

    const interval = setInterval(() => {
      setSecondsRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          handleFinishExam();
          return 0;
        }
        return prev - 1;
      });
      setTimeSpentSeconds((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [examStatus, secondsRemaining]);

  const handleStartExam = async () => {
    try {
      setLoading(true);
      const res = await startExam({
        numQuestions,
        durationMinutes
      });

      setSessionId(res.session_id);
      setExamQuestions(res.questions);
      setSecondsRemaining(res.duration_minutes * 60);
      setTimeSpentSeconds(0);
      setCurrentIndex(0);
      setUserAnswers({});
      setExamStatus('active');
    } catch (err) {
      console.error('Error al iniciar simulacro', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFinishExam = async () => {
    try {
      setLoading(true);
      const res = await submitExam(sessionId, userAnswers, timeSpentSeconds);
      setExamResults(res);
      setExamStatus('results');
      if (onRefreshDashboard) onRefreshDashboard();
    } catch (err) {
      console.error('Error al entregar simulacro', err);
    } finally {
      setLoading(false);
    }
  };

  const formatTimer = (totalSeconds: number) => {
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const currentQ = examQuestions[currentIndex];

  // 1. SETUP VIEW
  if (examStatus === 'setup') {
    return (
      <div className="max-w-3xl mx-auto space-y-6 pb-16">
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-navy-900 text-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-teal-50 text-teal-600 dark:bg-teal-950 dark:text-teal-400 mx-auto mb-4">
            <GraduationCap className="h-8 w-8" />
          </div>
          <h2 className="text-2xl font-black text-slate-900 dark:text-white">
            Simulador de Examen de Base de Datos I
          </h2>
          <p className="text-sm text-slate-600 dark:text-slate-400 max-w-xl mx-auto mt-2">
            Ponete a prueba bajo condiciones reales de examen: tiempo cronometrado estricto, preguntas aleatorias de todas las unidades y diagnóstico detallado de fortalezas y debilidades.
          </p>

          <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-6 text-left max-w-lg mx-auto">
            {/* Number of questions */}
            <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
              <label className="text-xs font-bold uppercase text-slate-500 block mb-2">
                Cantidad de Preguntas
              </label>
              <div className="grid grid-cols-3 gap-2">
                {[10, 15, 20].map((num) => (
                  <button
                    key={num}
                    onClick={() => setNumQuestions(num)}
                    className={`rounded-lg py-2 text-xs font-bold transition ${
                      numQuestions === num
                        ? 'bg-teal-600 text-white shadow'
                        : 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300'
                    }`}
                  >
                    {num}
                  </button>
                ))}
              </div>
            </div>

            {/* Duration */}
            <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
              <label className="text-xs font-bold uppercase text-slate-500 block mb-2">
                Límite de Tiempo
              </label>
              <div className="grid grid-cols-3 gap-2">
                {[20, 30, 45].map((mins) => (
                  <button
                    key={mins}
                    onClick={() => setDurationMinutes(mins)}
                    className={`rounded-lg py-2 text-xs font-bold transition ${
                      durationMinutes === mins
                        ? 'bg-teal-600 text-white shadow'
                        : 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300'
                    }`}
                  >
                    {mins}m
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-8">
            <button
              disabled={loading}
              onClick={handleStartExam}
              className="inline-flex items-center space-x-2 rounded-xl bg-teal-600 px-8 py-3.5 text-sm font-bold text-white shadow-lg hover:bg-teal-700 active:scale-95 disabled:opacity-50"
            >
              {loading ? (
                <span>Generando examen...</span>
              ) : (
                <>
                  <Sparkles className="h-4 w-4" />
                  <span>Comenzar Simulacro de Examen</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // 2. ACTIVE EXAM VIEW
  if (examStatus === 'active' && currentQ) {
    const isWarning = secondsRemaining < 300; // less than 5 min

    return (
      <div className="max-w-4xl mx-auto space-y-5 pb-16">
        {/* Sticky Top Status Bar */}
        <div className="sticky top-14 sm:top-16 z-20 flex items-center justify-between gap-2 rounded-2xl border border-slate-200 bg-white/95 p-3 sm:p-4 shadow-md backdrop-blur dark:border-slate-800 dark:bg-navy-900/95">
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold text-slate-700 dark:text-slate-200">
              {currentIndex + 1} <span className="text-slate-400">/ {examQuestions.length}</span>
            </span>
          </div>

          {/* Countdown Clock */}
          <div
            className={`flex items-center space-x-1.5 rounded-xl px-3 py-1.5 text-xs sm:text-sm font-black transition-colors ${
              isWarning
                ? 'bg-rose-100 text-rose-700 animate-pulse dark:bg-rose-950 dark:text-rose-400'
                : 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-200'
            }`}
          >
            <Clock className="h-3.5 w-3.5 sm:h-4 sm:w-4" />
            <span>{formatTimer(secondsRemaining)}</span>
          </div>

          <button
            onClick={handleFinishExam}
            className="rounded-xl bg-rose-600 px-3 py-1.5 text-xs font-bold text-white hover:bg-rose-700 active:scale-98 min-h-[36px]"
          >
            Entregar
          </button>
        </div>

        {/* Question Palette Navigation */}
        <div className="flex flex-wrap gap-1.5 justify-center max-h-24 sm:max-h-none overflow-y-auto p-1">
          {examQuestions.map((q, idx) => {
            const isAnswered = !!userAnswers[q.id];
            const isCurrent = idx === currentIndex;

            return (
              <button
                key={q.id}
                onClick={() => setCurrentIndex(idx)}
                className={`h-8 w-8 rounded-lg text-xs font-bold transition-all active:scale-95 ${
                  isCurrent
                    ? 'ring-2 ring-teal-500 bg-teal-600 text-white'
                    : isAnswered
                    ? 'bg-teal-100 text-teal-800 dark:bg-teal-950 dark:text-teal-300'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-400'
                }`}
              >
                {idx + 1}
              </button>
            );
          })}
        </div>

        {/* Question Viewport */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm dark:border-slate-800 dark:bg-navy-900 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3 dark:border-slate-800">
            <span className="rounded-md bg-teal-50 px-2.5 py-1 text-xs font-bold text-teal-700 dark:bg-teal-950 dark:text-teal-400">
              {currentQ.concept_name || 'Tema de Examen'}
            </span>
            <span className="text-xs text-slate-400">
              Tipo: {currentQ.type.replace('_', ' ')}
            </span>
          </div>

          <div className="text-base sm:text-lg font-bold text-slate-900 dark:text-white leading-snug">
            <MathText content={currentQ.question} />
          </div>

          {/* Options */}
          <div className="space-y-3 pt-2">
            {currentQ.type === 'multiple_choice' &&
              Array.isArray(currentQ.options) &&
              currentQ.options.map((opt: any, idx: number) => {
                const optId = opt.id || String.fromCharCode(65 + idx);
                const optText = opt.text || opt;
                const isSelected = userAnswers[currentQ.id] === optId;

                return (
                  <button
                    key={idx}
                    onClick={() =>
                      setUserAnswers((prev) => ({ ...prev, [currentQ.id]: optId }))
                    }
                    className={`flex items-start space-x-3 rounded-xl border p-4 text-left text-sm transition-all w-full ${
                      isSelected
                        ? 'border-teal-500 bg-teal-50 font-semibold text-teal-900 dark:bg-teal-950/40 dark:text-teal-200 shadow-sm'
                        : 'border-slate-200 hover:bg-slate-50 text-slate-800 dark:border-slate-800 dark:text-slate-200 dark:hover:bg-slate-800'
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

            {currentQ.type === 'true_false' && (
              <div className="grid grid-cols-2 gap-4">
                {['verdadero', 'falso'].map((val) => {
                  const isSelected = userAnswers[currentQ.id]?.toLowerCase() === val;
                  return (
                    <button
                      key={val}
                      onClick={() =>
                        setUserAnswers((prev) => ({ ...prev, [currentQ.id]: val }))
                      }
                      className={`rounded-2xl border p-6 text-center font-bold capitalize transition-all ${
                        isSelected
                          ? 'border-teal-500 bg-teal-50 text-teal-900 dark:bg-teal-950/40 dark:text-teal-200'
                          : 'border-slate-200 hover:bg-slate-50 text-slate-800 dark:border-slate-800 dark:text-slate-200'
                      }`}
                    >
                      {val}
                    </button>
                  );
                })}
              </div>
            )}

            {(currentQ.type === 'fill_blank' || currentQ.type === 'open_question') && (
              <textarea
                rows={3}
                value={userAnswers[currentQ.id] || ''}
                onChange={(e) =>
                  setUserAnswers((prev) => ({ ...prev, [currentQ.id]: e.target.value }))
                }
                placeholder="Escribí aquí tu respuesta..."
                className="w-full rounded-xl border border-slate-200 bg-slate-50 p-3.5 text-sm text-slate-900 focus:border-teal-500 focus:outline-none dark:border-slate-700 dark:bg-slate-800 dark:text-white"
              />
            )}
          </div>

          {/* Navigation Controls */}
          <div className="flex items-center justify-between border-t border-slate-100 pt-4 dark:border-slate-800">
            <button
              disabled={currentIndex === 0}
              onClick={() => setCurrentIndex((prev) => prev - 1)}
              className="inline-flex items-center space-x-1 rounded-xl border border-slate-200 px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 disabled:opacity-30 dark:border-slate-700 dark:text-slate-300"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Anterior</span>
            </button>

            <button
              disabled={currentIndex === examQuestions.length - 1}
              onClick={() => setCurrentIndex((prev) => prev + 1)}
              className="inline-flex items-center space-x-1 rounded-xl bg-teal-600 px-4 py-2 text-xs font-bold text-white hover:bg-teal-700 disabled:opacity-30"
            >
              <span>Siguiente</span>
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    );
  }

  // 3. RESULTS & DIAGNOSTIC VIEW
  if (examStatus === 'results' && examResults) {
    const { final_score_10, passed, grade_letter, correct_count, total_questions, diagnostic, details } = examResults;

    return (
      <div className="max-w-4xl mx-auto space-y-6 pb-16">
        {/* Results Banner */}
        <div
          className={`rounded-2xl border p-8 shadow-sm text-center ${
            passed
              ? 'border-emerald-200 bg-emerald-50/70 dark:border-emerald-900 dark:bg-emerald-950/30'
              : 'border-rose-200 bg-rose-50/70 dark:border-rose-900 dark:bg-rose-950/30'
          }`}
        >
          <div className="inline-flex items-center justify-center rounded-full p-3 mb-2">
            {passed ? (
              <CheckCircle className="h-12 w-12 text-emerald-600" />
            ) : (
              <AlertTriangle className="h-12 w-12 text-rose-600" />
            )}
          </div>
          <h2 className="text-2xl font-black text-slate-900 dark:text-white">
            {passed ? '¡Examen Aprobado!' : 'Examen Desaprobado — Necesitás Refuerzo'}
          </h2>
          <div className="mt-3 flex items-center justify-center space-x-4">
            <div className="text-4xl font-extrabold text-slate-900 dark:text-white">
              {final_score_10} <span className="text-base text-slate-500 font-medium">/ 10</span>
            </div>
            <span className="rounded-xl bg-slate-900 px-3 py-1 text-sm font-black text-white dark:bg-white dark:text-slate-900">
              {grade_letter}
            </span>
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-2">
            {correct_count} respuestas correctas de {total_questions} preguntas ({Math.round((correct_count / total_questions) * 100)}% de precisión).
          </p>

          <div className="mt-6 flex justify-center gap-3">
            <button
              onClick={() => setExamStatus('setup')}
              className="inline-flex items-center space-x-2 rounded-xl bg-white px-4 py-2 text-xs font-bold text-slate-700 shadow border border-slate-200 hover:bg-slate-50 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-200"
            >
              <RotateCcw className="h-3.5 w-3.5" />
              <span>Nuevo Simulacro</span>
            </button>
            <button
              onClick={() => onNavigateToPractice()}
              className="inline-flex items-center space-x-2 rounded-xl bg-teal-600 px-4 py-2 text-xs font-bold text-white shadow hover:bg-teal-700"
            >
              <BrainCircuit className="h-3.5 w-3.5" />
              <span>Practicar Errores Detectados</span>
            </button>
          </div>
        </div>

        {/* Diagnostic Strengths & Weaknesses */}
        {diagnostic && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Strengths */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-navy-900">
              <h3 className="font-bold text-emerald-700 dark:text-emerald-400 text-sm flex items-center space-x-2 mb-3">
                <CheckCircle className="h-4 w-4" />
                <span>Fortalezas Consolidadas</span>
              </h3>
              {diagnostic.strengths && diagnostic.strengths.length > 0 ? (
                <ul className="space-y-1.5 text-xs text-slate-700 dark:text-slate-300">
                  {diagnostic.strengths.map((s: string, i: number) => (
                    <li key={i} className="flex items-start space-x-2">
                      <span className="text-emerald-500 font-bold">✓</span>
                      <span>{s}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="text-xs text-slate-400">Continúa practicando para consolidar fortalezas.</div>
              )}
            </div>

            {/* Weaknesses */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-navy-900">
              <h3 className="font-bold text-rose-700 dark:text-rose-400 text-sm flex items-center space-x-2 mb-3">
                <AlertTriangle className="h-4 w-4" />
                <span>Temas Críticos a Reforzar</span>
              </h3>
              {diagnostic.weaknesses && diagnostic.weaknesses.length > 0 ? (
                <ul className="space-y-1.5 text-xs text-slate-700 dark:text-slate-300">
                  {diagnostic.weaknesses.map((w: string, i: number) => (
                    <li key={i} className="flex items-start space-x-2">
                      <span className="text-rose-500 font-bold">⚠</span>
                      <span>{w}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="text-xs text-slate-400">¡Ninguna debilidad crítica detectada!</div>
              )}
            </div>
          </div>
        )}

        {/* Question-by-Question Review */}
        <div className="space-y-4">
          <h3 className="text-base font-bold text-slate-900 dark:text-white px-1">
            Revisión Detallada Pregunta por Pregunta ({details?.length || 0})
          </h3>

          {details &&
            details.map((d: any, idx: number) => {
              return (
                <div
                  key={idx}
                  className={`rounded-2xl border p-5 shadow-sm transition-all ${
                    d.is_correct
                      ? 'border-emerald-200 bg-white dark:border-emerald-900/60 dark:bg-navy-900'
                      : 'border-rose-200 bg-white dark:border-rose-900/60 dark:bg-navy-900'
                  }`}
                >
                  <div className="flex items-center justify-between border-b border-slate-100 pb-2 dark:border-slate-800 mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-bold text-slate-400">#{idx + 1}</span>
                      <span className="text-xs font-semibold text-slate-600 dark:text-slate-300">
                        {d.concept_name || 'Pregunta de Examen'}
                      </span>
                    </div>
                    <div>
                      {d.is_correct ? (
                        <span className="inline-flex items-center space-x-1 text-xs font-bold text-emerald-600">
                          <CheckCircle className="h-3.5 w-3.5" />
                          <span>Correcta</span>
                        </span>
                      ) : (
                        <span className="inline-flex items-center space-x-1 text-xs font-bold text-rose-600">
                          <XCircle className="h-3.5 w-3.5" />
                          <span>Incorrecta</span>
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="text-sm font-bold text-slate-900 dark:text-white mb-3">
                    <MathText content={d.question} />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs mb-3">
                    <div className="rounded-xl bg-slate-50 p-3 dark:bg-slate-800">
                      <div className="text-slate-400 font-medium mb-0.5">Tu Respuesta:</div>
                      <div className={d.is_correct ? 'text-emerald-700 dark:text-emerald-400 font-semibold' : 'text-rose-700 dark:text-rose-400 font-semibold'}>
                        {d.user_answer || '(Sin responder)'}
                      </div>
                    </div>

                    <div className="rounded-xl bg-slate-50 p-3 dark:bg-slate-800">
                      <div className="text-slate-400 font-medium mb-0.5">Respuesta Correcta:</div>
                      <div className="text-slate-900 dark:text-white font-semibold">
                        {d.correct_answer}
                      </div>
                    </div>
                  </div>

                  {d.explanation && (
                    <div className="rounded-xl bg-teal-50/50 p-3 text-xs text-teal-950 dark:bg-teal-950/20 dark:text-teal-200 border border-teal-100 dark:border-teal-900/40">
                      <strong className="font-bold">Fundamento: </strong>
                      <MathText content={d.explanation} />
                    </div>
                  )}

                  {d.source_document && (
                    <div className="mt-2 text-[11px] text-slate-400">
                      Fuente: {d.source_document} (pág. {d.source_page})
                    </div>
                  )}
                </div>
              );
            })}
        </div>
      </div>
    );
  }

  return null;
};

export default ExamPage;
