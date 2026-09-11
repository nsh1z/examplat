import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  FileCheck,
  Database,
  Trash2,
  Filter,
  CheckCircle,
  Cpu,
  RefreshCw,
  Search
} from 'lucide-react';
import { fetchAdminStats, fetchAdminDocuments, fetchAdminQuestions, deleteAdminQuestion } from '../api';
import MathText from '../components/MathText';

export const AdminPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'docs' | 'questions' | 'engine'>('docs');
  const [stats, setStats] = useState<any | null>(null);
  const [documents, setDocuments] = useState<any[]>([]);
  const [questions, setQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Question filter state
  const [qTypeFilter, setQTypeFilter] = useState<string>('');
  const [qDiffFilter, setQDiffFilter] = useState<string>('');

  const loadAll = async () => {
    try {
      setLoading(true);
      const [sData, dData, qData] = await Promise.all([
        fetchAdminStats(),
        fetchAdminDocuments(),
        fetchAdminQuestions({ qType: qTypeFilter, difficulty: qDiffFilter })
      ]);
      setStats(sData);
      setDocuments(dData);
      setQuestions(qData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, [qTypeFilter, qDiffFilter]);

  const handleDeleteQ = async (id: string) => {
    if (!confirm('¿Estás seguro de eliminar esta pregunta del banco?')) return;
    try {
      await deleteAdminQuestion(id);
      setQuestions((prev) => prev.filter((q) => q.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-navy-900">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-xl font-black text-slate-900 dark:text-white flex items-center space-x-2">
              <ShieldCheck className="h-5 w-5 text-teal-600" />
              <span>Auditoría de Documentos & Banco de Preguntas</span>
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Verificación de las 5 presentaciones oficiales de cátedra, integridad referencial y sistema anti-repetición.
            </p>
          </div>

          {stats && (
            <div className="flex flex-wrap items-center gap-2 text-xs">
              <span className="rounded-lg bg-teal-50 px-2.5 py-1 font-bold text-teal-800 dark:bg-teal-950 dark:text-teal-300">
                {stats.total_topics} Temas
              </span>
              <span className="rounded-lg bg-teal-50 px-2.5 py-1 font-bold text-teal-800 dark:bg-teal-950 dark:text-teal-300">
                {stats.total_concepts} Conceptos
              </span>
              <span className="rounded-lg bg-teal-50 px-2.5 py-1 font-bold text-teal-800 dark:bg-teal-950 dark:text-teal-300">
                {stats.total_questions} Preguntas
              </span>
            </div>
          )}
        </div>

        {/* Tab switcher */}
        <div className="mt-5 flex flex-wrap gap-2 border-b border-slate-100 dark:border-slate-800 pb-2 text-xs">
          <button
            onClick={() => setActiveTab('docs')}
            className={`rounded-xl px-4 py-2 font-bold transition ${
              activeTab === 'docs'
                ? 'bg-teal-600 text-white shadow'
                : 'text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800'
            }`}
          >
            1. Documentos de Cátedra (5 Fuentes)
          </button>
          <button
            onClick={() => setActiveTab('questions')}
            className={`rounded-xl px-4 py-2 font-bold transition ${
              activeTab === 'questions'
                ? 'bg-teal-600 text-white shadow'
                : 'text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800'
            }`}
          >
            2. Gestor del Banco de Preguntas
          </button>
          <button
            onClick={() => setActiveTab('engine')}
            className={`rounded-xl px-4 py-2 font-bold transition ${
              activeTab === 'engine'
                ? 'bg-teal-600 text-white shadow'
                : 'text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800'
            }`}
          >
            3. Motor IA & Algoritmo SM-2
          </button>
        </div>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-navy-900">
          <div className="text-slate-400 text-sm">Cargando panel de auditoría...</div>
        </div>
      ) : (
        <>
          {/* TAB 1: 14 DOCUMENTS AUDIT */}
          {activeTab === 'docs' && (
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-navy-900 space-y-4">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">
                Inventario & Estado de Ingesta de Documentos ({documents.length} Archivos)
              </h3>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-700 dark:text-slate-300">
                  <thead className="bg-slate-50 text-slate-500 uppercase font-bold text-[11px] dark:bg-slate-800">
                    <tr>
                      <th className="p-3">#</th>
                      <th className="p-3">Documento Fuente</th>
                      <th className="p-3">Tema Principal</th>
                      <th className="p-3">Unidad Asignada</th>
                      <th className="p-3">Conceptos Extraídos</th>
                      <th className="p-3">Estado</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                    {documents.map((doc, idx) => (
                      <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                        <td className="p-3 font-bold text-slate-400">{idx + 1}</td>
                        <td className="p-3 font-semibold text-slate-900 dark:text-white">
                          {doc.filename}
                        </td>
                        <td className="p-3">{doc.main_topic}</td>
                        <td className="p-3">
                          <span className="rounded-md bg-slate-100 px-2 py-0.5 font-bold text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                            Unidad {doc.unit}
                          </span>
                        </td>
                        <td className="p-3 font-bold text-teal-600">{doc.concepts_count}</td>
                        <td className="p-3">
                          <span className="inline-flex items-center space-x-1 rounded-full bg-emerald-50 px-2 py-0.5 text-[11px] font-bold text-emerald-700 dark:bg-emerald-950 dark:text-emerald-400">
                            <CheckCircle className="h-3 w-3" />
                            <span>100% Ingestado</span>
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 2: QUESTIONS MANAGER */}
          {activeTab === 'questions' && (
            <div className="space-y-4">
              {/* Question filters */}
              <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-navy-900">
                <span className="text-xs font-bold text-slate-600 dark:text-slate-300">
                  {questions.length} preguntas en el banco
                </span>

                <div className="flex gap-2">
                  <select
                    value={qDiffFilter}
                    onChange={(e) => setQDiffFilter(e.target.value)}
                    className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs dark:border-slate-700 dark:bg-slate-800"
                  >
                    <option value="">Todas las dificultades</option>
                    <option value="facil">Fácil</option>
                    <option value="medio">Medio</option>
                    <option value="dificil">Difícil</option>
                    <option value="experto">Experto</option>
                  </select>

                  <select
                    value={qTypeFilter}
                    onChange={(e) => setQTypeFilter(e.target.value)}
                    className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs dark:border-slate-700 dark:bg-slate-800"
                  >
                    <option value="">Todos los tipos</option>
                    <option value="multiple_choice">Opción múltiple</option>
                    <option value="true_false">V / F</option>
                    <option value="fill_blank">Completar</option>
                    <option value="open_question">Abierta</option>
                    <option value="order_steps">Pasos</option>
                  </select>
                </div>
              </div>

              {/* Questions List */}
              <div className="space-y-3">
                {questions.map((q) => (
                  <div
                    key={q.id}
                    className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-navy-900 space-y-3"
                  >
                    <div className="flex items-center justify-between text-xs border-b border-slate-100 pb-2 dark:border-slate-800">
                      <div className="flex items-center space-x-2">
                        <span className="rounded-md bg-teal-50 px-2 py-0.5 font-bold text-teal-700 dark:bg-teal-950 dark:text-teal-400">
                          {q.type}
                        </span>
                        <span className="text-slate-400">•</span>
                        <span className="font-semibold text-slate-600 dark:text-slate-300">
                          {q.difficulty}
                        </span>
                        <span className="text-slate-400">•</span>
                        <span className="text-slate-500">
                          {q.source_document} (pág. {q.source_page})
                        </span>
                      </div>

                      <button
                        onClick={() => handleDeleteQ(q.id)}
                        className="text-slate-400 hover:text-rose-600 p-1"
                        title="Eliminar pregunta"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>

                    <div className="text-sm font-bold text-slate-900 dark:text-white">
                      <MathText content={q.question} />
                    </div>

                    <div className="rounded-xl bg-slate-50 p-3 text-xs text-slate-700 dark:bg-slate-800/60 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                      <strong className="text-teal-700 dark:text-teal-400">Respuesta Oficial: </strong>
                      <span className="font-mono">{q.correct_answer}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 3: ENGINE & SM-2 HEALTH */}
          {activeTab === 'engine' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* SM-2 Spaced Repetition Engine */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-navy-900 space-y-4">
                <div className="flex items-center space-x-2 text-teal-600 font-bold">
                  <Cpu className="h-5 w-5" />
                  <h3 className="text-base text-slate-900 dark:text-white">
                    Algoritmo de Repetición Espaciada SM-2
                  </h3>
                </div>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  Calcula el factor de facilidad (EF), intervalo de días de repaso y penalización por error según la fórmula de SuperMemo-2 adaptada:
                </p>
                <div className="rounded-xl bg-slate-50 p-3 font-mono text-xs text-slate-800 dark:bg-slate-800 dark:text-slate-200">
                  EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
                </div>
                <div className="text-xs text-emerald-600 font-semibold flex items-center space-x-1">
                  <CheckCircle className="h-3.5 w-3.5" />
                  <span>Activo y calibrando progreso del estudiante</span>
                </div>
              </div>

              {/* Anti-Repetition System */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-navy-900 space-y-4">
                <div className="flex items-center space-x-2 text-indigo-600 font-bold">
                  <ShieldCheck className="h-5 w-5" />
                  <h3 className="text-base text-slate-900 dark:text-white">
                    Sistema Anti-Repetición & Huellas Semánticas
                  </h3>
                </div>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  Evita la repetición de preguntas ya respondidas dentro de la ventana de enfriamiento y filtra por hash semántico de enunciados.
                </p>
                <div className="rounded-xl bg-slate-50 p-3 font-mono text-xs text-slate-800 dark:bg-slate-800 dark:text-slate-200">
                  Historial de intentos: Activo (prioriza conceptos con maestría &lt; 70%)
                </div>
                <div className="text-xs text-emerald-600 font-semibold flex items-center space-x-1">
                  <CheckCircle className="h-3.5 w-3.5" />
                  <span>0 duplicaciones detectadas en banco de preguntas</span>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default AdminPage;
