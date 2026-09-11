import React from 'react';
import {
  TrendingUp,
  CheckCircle2,
  Clock,
  AlertTriangle,
  Target,
  ArrowRight,
  BrainCircuit,
  GraduationCap,
  Database,
  BookOpen
} from 'lucide-react';
import { DashboardData } from '../types';
import { NavTab } from '../components/Sidebar';

interface DashboardPageProps {
  data: DashboardData | null;
  onNavigate: (tab: NavTab, params?: any) => void;
  onRefresh: () => void;
}

const UNIT_NAMES: Record<number, string> = {
  1: 'Unidad 1: Fundamentos de la Ingeniería de Datos y SGBD',
  2: 'Unidad 2: Modelado Conceptual — DER Clásico',
  3: 'Unidad 3: Modelo Entidad-Relación Extendido (EER)',
  4: 'Unidad 4: El Modelo Relacional y las 12 Reglas de Codd',
  5: 'Unidad 5: Álgebra Relacional Formal (16 Consultas)',
  6: 'Unidad 6: Metodología de Mapeo DER/EER a Esquema Relacional'
};

export const DashboardPage: React.FC<DashboardPageProps> = ({
  data,
  onNavigate
}) => {
  if (!data) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="text-center text-xs text-slate-500">
          <div className="h-6 w-6 animate-spin rounded-full border-2 border-slate-900 border-t-transparent dark:border-teal-500 mx-auto mb-2" />
          Cargando datos de estudio...
        </div>
      </div>
    );
  }

  const { stats, overall_progress_percent, continue_studying, unit_progress, weak_topics } = data;

  return (
    <div className="space-y-4 sm:space-y-6 pb-20 lg:pb-12 max-w-6xl mx-auto">
      {/* Header Banner - Clean & Academic */}
      <div className="rounded-xl border border-slate-200 bg-white p-4 sm:p-6 shadow-sm dark:border-slate-800 dark:bg-navy-900">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-teal-600 dark:text-teal-400">
              Temario Oficial — Examen
            </span>
            <h2 className="text-lg sm:text-xl font-extrabold text-slate-900 dark:text-white mt-0.5">
              Estado de Preparación
            </h2>
            <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 max-w-xl">
              Dominio general estimado: <strong className="text-slate-900 dark:text-white font-bold">{overall_progress_percent}%</strong> sobre los 5 documentos de cátedra (6 unidades).
            </p>
          </div>

          <div className="flex items-center gap-2 flex-shrink-0">
            <button
              onClick={() => onNavigate('practice')}
              className="inline-flex items-center space-x-1.5 rounded-lg bg-slate-900 px-3.5 py-2 text-xs font-bold text-white shadow-sm hover:bg-slate-800 dark:bg-teal-600 dark:hover:bg-teal-700 active:scale-[0.98] transition"
            >
              <BrainCircuit className="h-3.5 w-3.5" />
              <span>Practicar</span>
            </button>
            <button
              onClick={() => onNavigate('exam')}
              className="inline-flex items-center space-x-1.5 rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700 active:scale-[0.98] transition"
            >
              <GraduationCap className="h-3.5 w-3.5" />
              <span>Simulacro</span>
            </button>
          </div>
        </div>

        {/* Global Progress Bar */}
        <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800">
          <div className="flex items-center justify-between text-[11px] text-slate-500 mb-1.5">
            <span>Progreso Global</span>
            <span className="font-bold text-slate-700 dark:text-slate-300">{overall_progress_percent}%</span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
            <div
              className="h-full rounded-full bg-teal-600 transition-all duration-500"
              style={{ width: `${Math.max(4, overall_progress_percent)}%` }}
            />
          </div>
        </div>
      </div>

      {/* 4 Metrics Cards */}
      <div className="grid grid-cols-2 gap-2.5 sm:gap-4 lg:grid-cols-4">
        {/* Dominados */}
        <div className="rounded-xl border border-slate-200 bg-white p-3.5 sm:p-4 shadow-sm dark:border-slate-800 dark:bg-navy-900">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-[10px] sm:text-[11px] font-bold uppercase tracking-wider">
              Dominados
            </span>
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
          </div>
          <div className="mt-1 text-xl sm:text-2xl font-black text-slate-900 dark:text-white">
            {stats.dominados}
            <span className="text-xs font-normal text-slate-400 ml-1">/ {stats.total_concepts}</span>
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">&gt; 85% de maestría</div>
        </div>

        {/* En Progreso */}
        <div className="rounded-xl border border-slate-200 bg-white p-3.5 sm:p-4 shadow-sm dark:border-slate-800 dark:bg-navy-900">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-[10px] sm:text-[11px] font-bold uppercase tracking-wider">
              En Repaso
            </span>
            <Clock className="h-4 w-4 text-sky-600" />
          </div>
          <div className="mt-1 text-xl sm:text-2xl font-black text-slate-900 dark:text-white">
            {stats.en_progreso}
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">En asimilación activa</div>
        </div>

        {/* Por Reforzar */}
        <div className="rounded-xl border border-slate-200 bg-white p-3.5 sm:p-4 shadow-sm dark:border-slate-800 dark:bg-navy-900">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-[10px] sm:text-[11px] font-bold uppercase tracking-wider">
              Por Reforzar
            </span>
            <AlertTriangle className="h-4 w-4 text-rose-600" />
          </div>
          <div className="mt-1 text-xl sm:text-2xl font-black text-slate-900 dark:text-white">
            {stats.debiles}
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">Fallos o marcados</div>
        </div>

        {/* Precisión */}
        <div className="rounded-xl border border-slate-200 bg-white p-3.5 sm:p-4 shadow-sm dark:border-slate-800 dark:bg-navy-900">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-[10px] sm:text-[11px] font-bold uppercase tracking-wider">
              Precisión
            </span>
            <Target className="h-4 w-4 text-teal-600" />
          </div>
          <div className="mt-1 text-xl sm:text-2xl font-black text-slate-900 dark:text-white">
            {stats.accuracy_percent}%
          </div>
          <div className="text-[10px] text-slate-500 mt-0.5">{stats.total_correct} de {stats.total_attempts} aciertos</div>
        </div>
      </div>

      {/* Siguiente paso prioritario */}
      {continue_studying && (
        <div className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5 shadow-sm dark:border-slate-800 dark:bg-navy-900">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2.5 dark:border-slate-800 mb-3">
            <span className="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center space-x-1.5">
              <TrendingUp className="h-3.5 w-3.5 text-teal-600" />
              <span>Concepto Prioritario Recomendado (Repetición Espaciada)</span>
            </span>
          </div>

          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50 p-3.5 rounded-lg dark:bg-slate-800/60">
            <div>
              <span className="text-[10px] font-bold uppercase text-teal-700 dark:text-teal-400">
                Unidad {continue_studying.unit_number} • {continue_studying.topic_name}
              </span>
              <h4 className="text-sm font-bold text-slate-900 dark:text-white mt-0.5">
                {continue_studying.name}
              </h4>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => onNavigate('theory', { conceptId: continue_studying.id })}
                className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
              >
                Ver Teoría
              </button>
              <button
                onClick={() => onNavigate('practice', { topicId: continue_studying.id })}
                className="rounded-lg bg-teal-600 px-3 py-1.5 text-xs font-bold text-white hover:bg-teal-700"
              >
                Practicar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Dominio por Unidad (1 a 6) */}
      <div className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5 shadow-sm dark:border-slate-800 dark:bg-navy-900">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 px-0.5">
          Avance por Unidad Oficial
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {unit_progress.map((up) => {
            const unitTitle = UNIT_NAMES[up.unit] || `Unidad ${up.unit}`;
            return (
              <div
                key={up.unit}
                onClick={() => onNavigate('theory', { unitNumber: up.unit })}
                className="cursor-pointer rounded-lg border border-slate-200 p-3.5 transition hover:border-teal-500 hover:shadow-sm dark:border-slate-800 dark:hover:border-teal-600 dark:bg-slate-800/30"
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-bold text-teal-700 dark:text-teal-400">
                    U{up.unit}
                  </span>
                  <span className="text-xs font-bold text-slate-700 dark:text-slate-300">
                    {Math.round(up.mastery)}%
                  </span>
                </div>
                <div className="text-xs font-semibold text-slate-800 dark:text-slate-200 line-clamp-2 h-8">
                  {unitTitle.replace(`Unidad ${up.unit}: `, '')}
                </div>

                <div className="mt-2.5 h-1.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-700">
                  <div
                    className="h-full rounded-full bg-teal-600 transition-all duration-300"
                    style={{ width: `${Math.max(4, up.mastery)}%` }}
                  />
                </div>

                <div className="mt-2 flex items-center justify-between text-[10px] text-slate-400">
                  <span>{up.concept_count} conceptos</span>
                  <span className="text-teal-600 dark:text-teal-400 font-medium">Estudiar →</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Weak Points Card if any */}
      {weak_topics && weak_topics.length > 0 && (
        <div className="rounded-xl border border-rose-200 bg-white p-4 sm:p-5 shadow-sm dark:border-rose-900/40 dark:bg-navy-900">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-rose-700 dark:text-rose-400 flex items-center space-x-1.5">
              <AlertTriangle className="h-3.5 w-3.5" />
              <span>Temas con Mayor Tasa de Fallo</span>
            </h3>
            <button
              onClick={() => onNavigate('errors')}
              className="text-xs font-semibold text-rose-600 hover:underline"
            >
              Ver todos →
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {weak_topics.slice(0, 4).map((t, i) => (
              <div
                key={i}
                className="flex items-center justify-between rounded-lg bg-rose-50/60 p-2.5 text-xs dark:bg-rose-950/20 border border-rose-100 dark:border-rose-900/30"
              >
                <span className="font-medium text-slate-800 dark:text-slate-200 truncate pr-2">
                  {t.topic_name}
                </span>
                <span className="rounded bg-rose-100 px-1.5 py-0.5 text-[10px] font-bold text-rose-700 dark:bg-rose-900/60 dark:text-rose-300 flex-shrink-0">
                  {t.weak_count} fallos
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
