import React, { useState, useEffect } from 'react';
import {
  AlertCircle,
  BrainCircuit,
  TrendingDown,
  CheckCircle2,
  Calendar,
  FileText,
  RotateCcw,
  Trash2,
  X,
  AlertTriangle
} from 'lucide-react';
import { fetchErrors, resetErrors } from '../api';
import MathText from '../components/MathText';

interface ErrorsPageProps {
  onNavigateToPractice: (topicId?: string) => void;
  onRefreshDashboard?: () => void;
}

export const ErrorsPage: React.FC<ErrorsPageProps> = ({ onNavigateToPractice, onRefreshDashboard }) => {
  const [loading, setLoading] = useState<boolean>(true);
  const [resetting, setResetting] = useState<boolean>(false);
  const [showResetModal, setShowResetModal] = useState<boolean>(false);
  const [errorData, setErrorData] = useState<{
    weak_concepts: Array<{
      concept_id: string;
      concept_name: string;
      topic_name: string;
      topic_id: string;
      unit_number: number;
      mastery: number;
      status: string;
      source_document: string;
      source_page: string;
    }>;
    recent_failures: Array<{
      id: string;
      question_id: string;
      question_text: string;
      user_answer: string;
      concept_name: string;
      score: number;
      timestamp: string;
      explanation: string;
    }>;
  }>({
    weak_concepts: [],
    recent_failures: []
  });

  const loadData = async () => {
    try {
      setLoading(true);
      const data = await fetchErrors();
      if (Array.isArray(data)) {
        setErrorData({ weak_concepts: data, recent_failures: [] });
      } else if (data && typeof data === 'object') {
        setErrorData({
          weak_concepts: Array.isArray(data.weak_concepts) ? data.weak_concepts : [],
          recent_failures: Array.isArray(data.recent_failures) ? data.recent_failures : []
        });
      }
    } catch (err) {
      console.error('Error fetching errors', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleReset = async (mode: 'errors' | 'all') => {
    try {
      setResetting(true);
      await resetErrors(mode);
      await loadData();
      if (onRefreshDashboard) onRefreshDashboard();
      setShowResetModal(false);
    } catch (err) {
      console.error('Error resetting errors:', err);
      alert('Ocurrió un error al resetear los errores.');
    } finally {
      setResetting(false);
    }
  };

  const weakConcepts = errorData?.weak_concepts || [];
  const recentFailures = errorData?.recent_failures || [];

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-navy-900">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-black text-slate-900 dark:text-white flex items-center space-x-2">
              <AlertCircle className="h-5 w-5 text-rose-600" />
              <span>Centro de Errores & Refuerzo Prioritario</span>
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Registro de tus fallos y conceptos con maestría deficiente para estudio focalizado.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2 flex-shrink-0">
            {weakConcepts.length > 0 && (
              <button
                onClick={() => onNavigateToPractice()}
                className="inline-flex items-center space-x-2 rounded-xl bg-rose-600 px-4 py-2 text-xs font-bold text-white shadow hover:bg-rose-700 min-h-[40px]"
              >
                <BrainCircuit className="h-4 w-4" />
                <span>Practicar Todo lo Débil</span>
              </button>
            )}

            {(weakConcepts.length > 0 || recentFailures.length > 0) && (
              <button
                onClick={() => setShowResetModal(true)}
                className="inline-flex items-center space-x-2 rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2 text-xs font-bold text-slate-700 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-200 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-rose-950/40 dark:hover:text-rose-300 min-h-[40px] transition-colors"
                title="Resetear historial de errores"
              >
                <RotateCcw className="h-4 w-4" />
                <span>Resetear Errores</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-navy-900">
          <div className="text-slate-400 text-sm">Cargando registro de errores...</div>
        </div>
      ) : weakConcepts.length === 0 && recentFailures.length === 0 ? (
        <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center dark:border-slate-800 dark:bg-navy-900 shadow-sm">
          <CheckCircle2 className="h-12 w-12 text-emerald-500 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">
            ¡Tu historial está impecable!
          </h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1 mb-4">
            No tenés conceptos en estado crítico ni errores recientes pendientes de refuerzo.
          </p>
          <button
            onClick={() => onNavigateToPractice()}
            className="rounded-xl bg-teal-600 px-5 py-2 text-xs font-bold text-white hover:bg-teal-700"
          >
            Ir a la Práctica General
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Weak Concepts Grid */}
          {weakConcepts.length > 0 && (
            <div className="space-y-3">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 px-1">
                Conceptos con Bajo Nivel de Dominio ({weakConcepts.length})
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {weakConcepts.map((c) => (
                  <div
                    key={c.concept_id}
                    className="rounded-2xl border border-rose-200 bg-white p-5 shadow-sm dark:border-rose-900/60 dark:bg-navy-900 flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
                        <span>Unidad {c.unit_number}</span>
                        <span className="font-bold text-rose-600">
                          {Math.round(c.mastery)}% dominio
                        </span>
                      </div>
                      <h4 className="font-bold text-slate-900 dark:text-white text-sm">
                        {c.concept_name}
                      </h4>
                      <p className="text-xs text-slate-500 mt-0.5">{c.topic_name}</p>

                      <div className="mt-3 text-[11px] text-slate-400 flex items-center space-x-1">
                        <FileText className="h-3 w-3 text-slate-400" />
                        <span>
                          {c.source_document} (pág. {c.source_page})
                        </span>
                      </div>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800">
                      <button
                        onClick={() => onNavigateToPractice(c.topic_id)}
                        className="w-full rounded-xl bg-rose-50 px-3 py-1.5 text-xs font-bold text-rose-700 hover:bg-rose-100 dark:bg-rose-950/40 dark:text-rose-300"
                      >
                        Ejercitar este tema
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recent Failures History */}
          {recentFailures.length > 0 && (
            <div className="space-y-3">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 px-1">
                Historial de Intentos Fallidos Recientes
              </h3>
              <div className="space-y-3">
                {recentFailures.map((f) => (
                  <div
                    key={f.id}
                    className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-navy-900 space-y-3"
                  >
                    <div className="flex items-center justify-between text-xs border-b border-slate-100 pb-2 dark:border-slate-800">
                      <span className="font-bold text-slate-700 dark:text-slate-300">
                        {f.concept_name}
                      </span>
                      <span className="text-slate-400 flex items-center space-x-1">
                        <Calendar className="h-3 w-3" />
                        <span>{f.timestamp}</span>
                      </span>
                    </div>

                    <div className="text-sm font-semibold text-slate-900 dark:text-white">
                      <MathText content={f.question_text} />
                    </div>

                    <div className="rounded-xl bg-rose-50/70 p-3 text-xs text-rose-900 dark:bg-rose-950/30 dark:text-rose-300">
                      <strong className="font-bold">Tu respuesta registrada: </strong>
                      <span>{f.user_answer}</span>
                    </div>

                    {f.explanation && (
                      <div className="rounded-xl bg-slate-50 p-3 text-xs text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                        <strong className="font-bold text-teal-800 dark:text-teal-300">Fundamento: </strong>
                        <MathText content={f.explanation} />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Modal de Confirmación de Reseteo */}
      {showResetModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl dark:border-slate-800 dark:bg-navy-900 space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <div className="flex items-center space-x-2 text-rose-600 font-black text-base">
                <AlertTriangle className="h-5 w-5" />
                <span>Resetear Historial de Errores</span>
              </div>
              <button
                onClick={() => setShowResetModal(false)}
                className="rounded-lg p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
              Seleccioná cómo deseás restablecer tu registro de práctica:
            </p>

            <div className="space-y-3">
              {/* Opción 1: Solo Errores */}
              <button
                disabled={resetting}
                onClick={() => handleReset('errors')}
                className="w-full text-left p-4 rounded-xl border border-rose-200 bg-rose-50/60 hover:bg-rose-100/70 dark:border-rose-900/60 dark:bg-rose-950/30 dark:hover:bg-rose-950/50 transition-all group"
              >
                <div className="flex items-center justify-between">
                  <div className="font-bold text-sm text-rose-900 dark:text-rose-200 flex items-center space-x-2">
                    <RotateCcw className="h-4 w-4 text-rose-600" />
                    <span>Limpiar solo fallos y errores</span>
                  </div>
                  <span className="text-[10px] font-bold uppercase tracking-wider bg-rose-200/60 text-rose-800 dark:bg-rose-900/60 dark:text-rose-200 px-2 py-0.5 rounded-full">
                    Recomendado
                  </span>
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 pl-6">
                  Elimina los intentos incorrectos y desmarca los conceptos débiles para limpiar la vista. Mantiene tu XP acumulada y respuestas acertadas.
                </p>
              </button>

              {/* Opción 2: Reset Completo */}
              <button
                disabled={resetting}
                onClick={() => {
                  if (confirm('¿Confirmás que querés borrar TODO tu progreso (XP, historial de simulacros y prácticas)?')) {
                    handleReset('all');
                  }
                }}
                className="w-full text-left p-4 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100 dark:border-slate-800 dark:bg-slate-800/60 dark:hover:bg-slate-800 transition-all"
              >
                <div className="font-bold text-sm text-slate-800 dark:text-slate-200 flex items-center space-x-2">
                  <Trash2 className="h-4 w-4 text-slate-500" />
                  <span>Reiniciar todo a cero</span>
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 pl-6">
                  Borra todos los intentos, sesiones de examen y resetea tu nivel y XP a 0.
                </p>
              </button>
            </div>

            <div className="flex justify-end pt-2">
              <button
                type="button"
                disabled={resetting}
                onClick={() => setShowResetModal(false)}
                className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ErrorsPage;
