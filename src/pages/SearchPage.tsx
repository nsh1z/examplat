import React, { useState } from 'react';
import {
  Search,
  ArrowRightLeft,
  FileText,
  BookOpen,
  HelpCircle,
  Sparkles,
  ExternalLink
} from 'lucide-react';
import { searchKnowledge } from '../api';
import MathText from '../components/MathText';
import { NavTab } from '../components/Sidebar';

interface SearchPageProps {
  onNavigateToTheory: (topicId?: string, conceptId?: string) => void;
}

const COMMON_COMPARISONS = [
  'Clave Primaria vs Clave Candidata',
  'Especialización vs Generalización',
  'Restricción d (disjunta) vs o (superpuesta)',
  'Total vs Parcial (Completitud)',
  'Join Natural vs Producto Cartesiano',
  'Mapeo 1:N vs Mapeo N:M'
];

export const SearchPage: React.FC<SearchPageProps> = ({ onNavigateToTheory }) => {
  const [query, setQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [results, setResults] = useState<{
    query: string;
    is_comparison?: boolean;
    comparison_data?: any;
    concepts: any[];
  } | null>(null);

  const handleSearch = async (term?: string) => {
    const q = term !== undefined ? term : query;
    if (!q.trim()) return;

    try {
      setLoading(true);
      const data = await searchKnowledge(q);
      setResults(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-16">
      {/* Search Header */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm dark:border-slate-800 dark:bg-navy-900 text-center">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-teal-50 text-teal-600 dark:bg-teal-950 dark:text-teal-400 mx-auto mb-3">
          <Search className="h-6 w-6" />
        </div>
        <h2 className="text-xl font-black text-slate-900 dark:text-white">
          Buscador Conceptual & Comparador
        </h2>
        <p className="text-xs text-slate-500 max-w-md mx-auto mt-1">
          Buscá cualquier concepto oficial del curso o compará dos conceptos escribiendo "vs" (ej: "disjunta vs superpuesta").
        </p>

        {/* Search Input */}
        <div className="mt-6 flex items-center max-w-xl mx-auto rounded-2xl border border-slate-200 bg-slate-50 p-1.5 dark:border-slate-700 dark:bg-slate-800 shadow-inner">
          <Search className="h-5 w-5 text-slate-400 ml-3 mr-2 flex-shrink-0" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ej: 'DROP vs TRUNCATE', 'Normalización', 'HAVING'..."
            className="w-full bg-transparent text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none dark:text-white"
          />
          <button
            onClick={() => handleSearch()}
            disabled={loading}
            className="rounded-xl bg-teal-600 px-5 py-2 text-xs font-bold text-white shadow hover:bg-teal-700 disabled:opacity-50 flex-shrink-0"
          >
            {loading ? 'Buscando...' : 'Buscar'}
          </button>
        </div>

        {/* Common comparison pills */}
        <div className="mt-4 flex flex-wrap items-center justify-center gap-2">
          <span className="text-[11px] text-slate-400">Comparaciones rápidas:</span>
          {COMMON_COMPARISONS.map((comp) => (
            <button
              key={comp}
              onClick={() => {
                setQuery(comp);
                handleSearch(comp);
              }}
              className="rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-[11px] font-medium text-slate-600 hover:border-teal-500 hover:text-teal-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
            >
              {comp}
            </button>
          ))}
        </div>
      </div>

      {/* Results Section */}
      {loading ? (
        <div className="flex h-48 items-center justify-center rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-navy-900">
          <div className="text-slate-400 text-sm">Explorando base de conocimiento...</div>
        </div>
      ) : results ? (
        <div className="space-y-6">
          {/* 1. Side-by-side comparison table if comparison mode triggered */}
          {results.is_comparison && results.comparison_data && (
            <div className="rounded-2xl border border-teal-200 bg-teal-50/40 p-6 dark:border-teal-900 dark:bg-teal-950/20 shadow-sm space-y-4">
              <div className="flex items-center space-x-2 text-teal-800 dark:text-teal-300 font-bold text-sm">
                <ArrowRightLeft className="h-4 w-4" />
                <span>Cuadro Comparativo: {results.comparison_data.title}</span>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left text-slate-700 dark:text-slate-300">
                  <thead className="bg-teal-100/70 dark:bg-teal-900/60 text-teal-900 dark:text-teal-200 font-bold uppercase">
                    <tr>
                      <th className="p-3 rounded-l-lg">Criterio / Característica</th>
                      <th className="p-3">{results.comparison_data.concept_a.name}</th>
                      <th className="p-3 rounded-r-lg">{results.comparison_data.concept_b.name}</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-teal-100 dark:divide-teal-900/40">
                    {results.comparison_data.rows.map((row: any, i: number) => (
                      <tr key={i} className="hover:bg-white/60 dark:hover:bg-slate-800/40">
                        <td className="p-3 font-semibold text-slate-900 dark:text-white">
                          {row.criterion}
                        </td>
                        <td className="p-3 font-mono text-[11px]">{row.a_val}</td>
                        <td className="p-3 font-mono text-[11px]">{row.b_val}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {results.comparison_data.summary && (
                <div className="rounded-xl bg-white p-3.5 text-xs text-slate-700 dark:bg-slate-800 dark:text-slate-200 border border-teal-200 dark:border-teal-800">
                  <strong className="font-bold text-teal-800 dark:text-teal-300">Resumen clave para examen: </strong>
                  {results.comparison_data.summary}
                </div>
              )}
            </div>
          )}

          {/* 2. Concepts Search Results */}
          <div className="space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 px-1">
              Resultados Conceptuales ({results.concepts.length})
            </h3>

            {results.concepts.length > 0 ? (
              results.concepts.map((c) => (
                <div
                  key={c.id}
                  className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-navy-900 space-y-3"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2 dark:border-slate-800">
                    <div>
                      <span className="text-[11px] font-bold uppercase text-teal-600">
                        Unidad {c.unit_number} • {c.topic_name}
                      </span>
                      <h4 className="text-base font-bold text-slate-900 dark:text-white">
                        {c.name}
                      </h4>
                    </div>

                    <button
                      onClick={() => onNavigateToTheory(c.topic_id, c.id)}
                      className="inline-flex items-center space-x-1 text-xs font-bold text-teal-600 hover:text-teal-700 dark:text-teal-400"
                    >
                      <span>Abrir en Teoría</span>
                      <ExternalLink className="h-3 w-3" />
                    </button>
                  </div>

                  <div className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
                    <MathText content={c.definition} />
                  </div>

                  {c.simple_explanation && (
                    <div className="rounded-xl bg-slate-50 p-3 text-xs text-slate-600 dark:bg-slate-800/60 dark:text-slate-400">
                      <strong className="text-slate-800 dark:text-slate-200">En pocas palabras: </strong>
                      <MathText content={c.simple_explanation} />
                    </div>
                  )}

                  <div className="text-[11px] text-slate-400 flex items-center space-x-1 pt-1">
                    <FileText className="h-3 w-3" />
                    <span>
                      {c.source_document} (pág. {c.source_page})
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center text-slate-400 dark:border-slate-800 dark:bg-navy-900">
                No se encontraron conceptos con ese criterio. Probá con otra palabra clave.
              </div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default SearchPage;
