import React, { useState, useEffect } from 'react';
import {
  Database,
  Code2,
  CheckCircle,
  Copy,
  Check,
  ChevronDown,
  ChevronRight,
  FileText,
  Eye,
  Terminal,
  Play
} from 'lucide-react';
import { CaseStudy } from '../types';
import { fetchCases, fetchCaseDetail } from '../api';
import MathText from '../components/MathText';

export const CasesPage: React.FC = () => {
  const [cases, setCases] = useState<CaseStudy[]>([]);
  const [selectedCaseId, setSelectedCaseId] = useState<string>('algebra');
  const [currentCase, setCurrentCase] = useState<CaseStudy | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Expanded solutions and user draft code state
  const [revealedSolutions, setRevealedSolutions] = useState<Record<number, boolean>>({});
  const [userDrafts, setUserDrafts] = useState<Record<number, string>>({});
  const [copiedDDL, setCopiedDDL] = useState<boolean>(false);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const data = await fetchCases();
        setCases(data);
        if (data.length > 0) {
          const initialId = data[0].id;
          setSelectedCaseId(initialId);
          const detail = await fetchCaseDetail(initialId);
          setCurrentCase(detail);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const handleSelectCase = async (id: string) => {
    try {
      setSelectedCaseId(id);
      setLoading(true);
      setRevealedSolutions({});
      const detail = await fetchCaseDetail(id);
      setCurrentCase(detail);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const copyDDL = () => {
    if (currentCase?.schema_ddl) {
      navigator.clipboard.writeText(currentCase.schema_ddl);
      setCopiedDDL(true);
      setTimeout(() => setCopiedDDL(false), 2000);
    }
  };

  const toggleSolution = (num: number) => {
    setRevealedSolutions((prev) => ({
      ...prev,
      [num]: !prev[num]
    }));
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-navy-900">
        <h2 className="text-xl font-black text-slate-900 dark:text-white flex items-center space-x-2">
          <Database className="h-5 w-5 text-teal-600" />
          <span>Casos Prácticos & Álgebra Relacional</span>
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Ejercicios y casos de estudio extraídos de las diapositivas oficiales: 16 consultas formales de Álgebra Relacional, Caso Constructora y Mapeo DER/EER.
        </p>

        {/* Case selector tabs */}
        <div className="mt-5 flex flex-wrap gap-2">
          {cases.map((c) => {
            const isSelected = c.id === selectedCaseId;
            return (
              <button
                key={c.id}
                onClick={() => handleSelectCase(c.id)}
                className={`rounded-xl px-4 py-2.5 text-xs font-bold transition active:scale-98 min-h-[40px] ${
                  isSelected
                    ? 'bg-teal-600 text-white shadow-md shadow-teal-600/20'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700'
                }`}
              >
                {c.title}
              </button>
            );
          })}
        </div>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-navy-900">
          <div className="text-slate-400 text-sm">Cargando caso práctico...</div>
        </div>
      ) : currentCase ? (
        <div className="space-y-6">
          {/* Overview & DDL Box */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-navy-900">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4 dark:border-slate-800">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-teal-600">
                  {currentCase.category}
                </span>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white">
                  {currentCase.title}
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                  {currentCase.description}
                </p>
              </div>

              <div className="flex items-center space-x-2">
                <span className="inline-flex items-center space-x-1 rounded-md bg-slate-100 px-2.5 py-1 text-[11px] font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                  <FileText className="h-3 w-3 text-slate-400" />
                  <span>{currentCase.source_document}</span>
                </span>
              </div>
            </div>

            {/* Schema DDL / Syntax Reference */}
            {currentCase.schema_ddl && (
              <div className="mt-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold uppercase text-slate-400 flex items-center space-x-1">
                    <Terminal className="h-3.5 w-3.5" />
                    <span>Esquema DDL / Tablas del Caso</span>
                  </span>
                  <button
                    onClick={copyDDL}
                    className="inline-flex items-center space-x-1 rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300"
                  >
                    {copiedDDL ? (
                      <>
                        <Check className="h-3.5 w-3.5 text-emerald-600" />
                        <span>¡Copiado!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="h-3.5 w-3.5" />
                        <span>Copiar Esquema SQL</span>
                      </>
                    )}
                  </button>
                </div>
                <div className="rounded-xl bg-slate-900 p-4 text-emerald-400 font-mono text-xs overflow-x-auto max-h-56">
                  <pre className="whitespace-pre-wrap">{currentCase.schema_ddl}</pre>
                </div>
              </div>
            )}
          </div>

          {/* Queries / Exercises Section */}
          <div className="space-y-4">
            <h3 className="text-base font-bold text-slate-900 dark:text-white px-1">
              Catálogo de Consultas & Ejercicios ({currentCase.sample_queries?.length || 0})
            </h3>

            {currentCase.sample_queries && currentCase.sample_queries.length > 0 ? (
              currentCase.sample_queries.map((q) => {
                const isRevealed = revealedSolutions[q.num];
                const draft = userDrafts[q.num] || '';

                return (
                  <div
                    key={q.num}
                    className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-navy-900 transition-all hover:border-slate-300 dark:hover:border-slate-700 space-y-4"
                  >
                    <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                      <div className="flex items-start space-x-3">
                        <span className="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-lg bg-teal-100 text-xs font-bold text-teal-800 dark:bg-teal-950 dark:text-teal-300">
                          #{q.num}
                        </span>
                        <div>
                          <div className="text-sm font-bold text-slate-900 dark:text-white">
                            <MathText content={q.prompt} />
                          </div>
                        </div>
                      </div>

                      <button
                        onClick={() => toggleSolution(q.num)}
                        className="inline-flex items-center space-x-1.5 rounded-xl border border-slate-200 px-3 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 active:scale-98 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800 flex-shrink-0 self-start sm:self-auto min-h-[38px]"
                      >
                        <Eye className="h-3.5 w-3.5 text-teal-600" />
                        <span>{isRevealed ? 'Ocultar Solución' : 'Ver Solución Oficial'}</span>
                      </button>
                    </div>

                    {/* Interactive SQL / Formula Scratchpad */}
                    <div className="rounded-xl border border-slate-200 bg-slate-50/70 p-3 dark:border-slate-800 dark:bg-slate-800/40">
                      <div className="text-[11px] font-bold text-slate-500 uppercase mb-1 flex items-center space-x-1">
                        <Code2 className="h-3.5 w-3.5" />
                        <span>Espacio de Trabajo / Tu Consulta:</span>
                      </div>
                      <textarea
                        rows={2}
                        value={draft}
                        onChange={(e) =>
                          setUserDrafts((prev) => ({ ...prev, [q.num]: e.target.value }))
                        }
                        placeholder="Escribí aquí tu propuesta de consulta SQL o fórmula algebraica antes de ver la solución..."
                        className="w-full rounded-lg border border-slate-200 bg-white p-2.5 font-mono text-xs text-slate-800 focus:border-teal-500 focus:outline-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200"
                      />
                    </div>

                    {/* Solution Reveal Accordion */}
                    {isRevealed && (
                      <div className="rounded-xl border border-teal-200 bg-teal-50/50 p-4 dark:border-teal-900/60 dark:bg-teal-950/20 space-y-2">
                        <div className="text-xs font-bold text-teal-900 dark:text-teal-300 uppercase">
                          Solución Oficial:
                        </div>
                        <div className="rounded-lg bg-slate-900 p-3 text-emerald-400 font-mono text-xs overflow-x-auto">
                          {currentCase.id === 'algebra' ? (
                            <MathText content={q.solution} block />
                          ) : (
                            <pre className="whitespace-pre-wrap">{q.solution}</pre>
                          )}
                        </div>
                        {q.explanation && (
                          <div className="text-xs text-slate-700 dark:text-slate-300 pt-1">
                            <strong className="text-teal-950 dark:text-teal-200">Explicación técnica: </strong>
                            <MathText content={q.explanation} />
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })
            ) : (
              <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center text-slate-400">
                No hay consultas registradas para este caso.
              </div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default CasesPage;
