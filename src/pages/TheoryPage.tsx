import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  ChevronRight,
  CheckCircle,
  AlertCircle,
  BrainCircuit,
  FileText,
  Bookmark,
  Check,
  Filter
} from 'lucide-react';
import { UnitGroup, Concept, Topic } from '../types';
import { fetchUnits, fetchTopicDetail, setConceptFeedback, saveConceptNote } from '../api';
import MathText from '../components/MathText';

interface TheoryPageProps {
  initialUnitNumber?: number;
  initialConceptId?: string;
  onNavigateToPractice: (topicId?: string, conceptId?: string) => void;
}

export const TheoryPage: React.FC<TheoryPageProps> = ({
  initialUnitNumber,
  initialConceptId,
  onNavigateToPractice
}) => {
  const [units, setUnits] = useState<UnitGroup[]>([]);
  const [selectedUnit, setSelectedUnit] = useState<number>(initialUnitNumber || 1);
  const [selectedTopicId, setSelectedTopicId] = useState<string>('');
  const [currentTopic, setCurrentTopic] = useState<(Topic & { concepts: Concept[] }) | null>(null);
  const [loadingUnits, setLoadingUnits] = useState<boolean>(true);
  const [loadingTopic, setLoadingTopic] = useState<boolean>(false);

  // Concept state
  const [conceptFeedbackState, setConceptFeedbackState] = useState<Record<string, string>>({});
  const [notesState, setNotesState] = useState<Record<string, string>>({});
  const [savedNotesMessage, setSavedNotesMessage] = useState<Record<string, boolean>>({});
  const [activeTabByConcept, setActiveTabByConcept] = useState<Record<string, 'formal' | 'simple' | 'example'>>({});

  useEffect(() => {
    async function load() {
      try {
        setLoadingUnits(true);
        const data = await fetchUnits();
        setUnits(data);

        const unit = data.find((u) => u.unit_number === selectedUnit) || data[0];
        if (unit && unit.topics.length > 0) {
          setSelectedUnit(unit.unit_number);
          setSelectedTopicId(unit.topics[0].id);
        }
      } catch (err) {
        console.error('Error al cargar unidades', err);
      } finally {
        setLoadingUnits(false);
      }
    }
    load();
  }, []);

  useEffect(() => {
    if (!selectedTopicId) return;
    async function loadTopic() {
      try {
        setLoadingTopic(true);
        const detail = await fetchTopicDetail(selectedTopicId);
        setCurrentTopic(detail);

        const initialNotes: Record<string, string> = {};
        const feedbackInit: Record<string, string> = {};
        detail.concepts.forEach((c) => {
          if (c.note_text) initialNotes[c.id] = c.note_text;
          if (c.user_status) feedbackInit[c.id] = c.user_status;
        });
        setNotesState((prev) => ({ ...prev, ...initialNotes }));
        setConceptFeedbackState((prev) => ({ ...prev, ...feedbackInit }));

        if (initialConceptId) {
          setTimeout(() => {
            const el = document.getElementById(`concept-${initialConceptId}`);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }, 300);
        }
      } catch (err) {
        console.error('Error al cargar tema', err);
      } finally {
        setLoadingTopic(false);
      }
    }
    loadTopic();
  }, [selectedTopicId]);

  const handleUnitSelect = (unitNum: number) => {
    setSelectedUnit(unitNum);
    const unit = units.find((u) => u.unit_number === unitNum);
    if (unit && unit.topics.length > 0) {
      setSelectedTopicId(unit.topics[0].id);
    }
  };

  const handleFeedback = async (conceptId: string, action: 'entendido' | 'practicar') => {
    try {
      setConceptFeedbackState((prev) => ({
        ...prev,
        [conceptId]: action === 'entendido' ? 'dominado' : 'debil'
      }));
      await setConceptFeedback(conceptId, action);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSaveNote = async (conceptId: string) => {
    try {
      const text = notesState[conceptId] || '';
      await saveConceptNote(conceptId, text);
      setSavedNotesMessage((prev) => ({ ...prev, [conceptId]: true }));
      setTimeout(() => {
        setSavedNotesMessage((prev) => ({ ...prev, [conceptId]: false }));
      }, 2000);
    } catch (err) {
      console.error(err);
    }
  };

  if (loadingUnits) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="text-center text-xs text-slate-500">
          <div className="h-6 w-6 animate-spin rounded-full border-2 border-slate-900 border-t-transparent dark:border-teal-500 mx-auto mb-2" />
          Cargando unidades temáticas...
        </div>
      </div>
    );
  }

  const currentUnitObj = units.find((u) => u.unit_number === selectedUnit);

  return (
    <div className="space-y-4 sm:space-y-6 pb-24 lg:pb-16 max-w-6xl mx-auto">
      {/* Unit Selector Header - Clean Horizontal Scroll for Mobile */}
      <div className="overflow-x-auto pb-1 scrollbar-none -mx-2 px-2 sm:mx-0 sm:px-0">
        <div className="flex space-x-1.5 sm:space-x-2 min-w-max">
          {units.map((u) => {
            const isSelected = u.unit_number === selectedUnit;
            return (
              <button
                key={u.unit_number}
                onClick={() => handleUnitSelect(u.unit_number)}
                className={`flex items-center space-x-1.5 rounded-lg px-3 py-2 text-xs font-semibold transition ${
                  isSelected
                    ? 'bg-slate-900 text-white dark:bg-teal-600 dark:text-white shadow-sm'
                    : 'bg-white text-slate-700 hover:bg-slate-100 dark:bg-navy-900 dark:text-slate-300 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800'
                }`}
              >
                <span className="font-bold">U{u.unit_number}</span>
                <span className="hidden sm:inline font-normal text-[11px]">
                  {u.title.replace(`Unidad ${u.unit_number}: `, '').split('—')[0].split(':')[0]}
                </span>
                <span className="rounded bg-black/10 dark:bg-white/10 px-1 py-0.2 text-[10px]">
                  {u.topics.length}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Grid: Left Topics (hidden or collapsible on mobile) + Right Concepts */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-4">
        {/* Topics Selector: On Mobile, a clean dropdown / list */}
        <div className="lg:col-span-1 space-y-2">
          {/* Mobile dropdown for topic selector */}
          <div className="lg:hidden rounded-xl border border-slate-200 bg-white p-3 shadow-sm dark:border-slate-800 dark:bg-navy-900">
            <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1.5">
              Tema de la Unidad {selectedUnit}
            </label>
            <select
              value={selectedTopicId}
              onChange={(e) => setSelectedTopicId(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-slate-50 p-2 text-xs text-slate-800 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
            >
              {currentUnitObj?.topics.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name} ({t.concept_count || 0} conceptos)
                </option>
              ))}
            </select>
          </div>

          {/* Desktop Topics List */}
          <div className="hidden lg:block rounded-xl border border-slate-200 bg-white p-3 dark:border-slate-800 dark:bg-navy-900 shadow-sm">
            <div className="px-2 pb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
              Temas Unidad {selectedUnit}
            </div>
            <div className="space-y-1">
              {currentUnitObj?.topics.map((t) => {
                const isActive = t.id === selectedTopicId;
                return (
                  <button
                    key={t.id}
                    onClick={() => setSelectedTopicId(t.id)}
                    className={`w-full text-left rounded-lg p-2.5 text-xs transition flex items-start justify-between ${
                      isActive
                        ? 'bg-slate-100 text-slate-900 font-bold dark:bg-slate-800 dark:text-white'
                        : 'text-slate-600 hover:bg-slate-50 dark:text-slate-400 dark:hover:bg-slate-800/60'
                    }`}
                  >
                    <div>
                      <div className="line-clamp-2">{t.name}</div>
                      <div className="text-[10px] font-normal text-slate-400 mt-0.5">
                        {t.concept_count || 0} conceptos
                      </div>
                    </div>
                    {isActive && <ChevronRight className="h-4 w-4 text-teal-600 flex-shrink-0 mt-0.5 ml-1" />}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right: Concepts View */}
        <div className="lg:col-span-3 space-y-4 sm:space-y-6">
          {loadingTopic ? (
            <div className="flex h-48 items-center justify-center rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-navy-900">
              <div className="text-slate-400 text-xs">Cargando conceptos...</div>
            </div>
          ) : currentTopic ? (
            <>
              {/* Topic Header Card */}
              <div className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5 shadow-sm dark:border-slate-800 dark:bg-navy-900">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-teal-600 dark:text-teal-400">
                      Unidad {selectedUnit} • {currentTopic.name}
                    </span>
                    <h2 className="text-base sm:text-lg font-black text-slate-900 dark:text-white mt-0.5">
                      {currentTopic.name}
                    </h2>
                    {currentTopic.description && (
                      <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                        {currentTopic.description}
                      </p>
                    )}
                  </div>
                  <button
                    onClick={() => onNavigateToPractice(currentTopic.id)}
                    className="inline-flex items-center space-x-1.5 rounded-lg bg-teal-600 px-3.5 py-1.5 text-xs font-bold text-white hover:bg-teal-700 active:scale-[0.98] self-start sm:self-auto flex-shrink-0 transition"
                  >
                    <BrainCircuit className="h-3.5 w-3.5" />
                    <span>Practicar Tema</span>
                  </button>
                </div>
              </div>

              {/* Concepts List */}
              <div className="space-y-4">
                {currentTopic.concepts && currentTopic.concepts.length > 0 ? (
                  currentTopic.concepts.map((concept, index) => {
                    const activeTab = activeTabByConcept[concept.id] || 'formal';
                    const feedback = conceptFeedbackState[concept.id];

                    return (
                      <div
                        key={concept.id}
                        id={`concept-${concept.id}`}
                        className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5 shadow-sm dark:border-slate-800 dark:bg-navy-900 space-y-3"
                      >
                        {/* Concept Header */}
                        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2.5 dark:border-slate-800">
                          <div className="flex items-center space-x-2">
                            <span className="flex h-5 w-5 items-center justify-center rounded bg-slate-100 text-[11px] font-bold text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                              {index + 1}
                            </span>
                            <h3 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white">
                              {concept.name}
                            </h3>
                          </div>

                          <div className="flex items-center space-x-1.5">
                            {/* PDF Citation */}
                            <span
                              className="inline-flex items-center space-x-1 rounded bg-slate-100 px-2 py-0.5 text-[10px] font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300"
                              title={`Fuente: ${concept.source_document}, pág. ${concept.source_page}`}
                            >
                              <FileText className="h-2.5 w-2.5 text-slate-400" />
                              <span className="max-w-[140px] truncate">{concept.source_document}</span>
                              <span>(pág. {concept.source_page})</span>
                            </span>

                            {/* Difficulty */}
                            <span
                              className={`rounded px-1.5 py-0.5 text-[10px] font-bold uppercase ${
                                concept.difficulty === 'facil'
                                  ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-400'
                                  : concept.difficulty === 'medio'
                                  ? 'bg-sky-50 text-sky-700 dark:bg-sky-950 dark:text-sky-400'
                                  : 'bg-amber-50 text-amber-700 dark:bg-amber-950 dark:text-amber-400'
                              }`}
                            >
                              {concept.difficulty}
                            </span>
                          </div>
                        </div>

                        {/* 3-Level Tabs (Formal, Simple, Ejemplo) */}
                        <div>
                          <div className="flex space-x-1 border-b border-slate-100 pb-1.5 dark:border-slate-800 text-xs">
                            <button
                              onClick={() =>
                                setActiveTabByConcept((prev) => ({ ...prev, [concept.id]: 'formal' }))
                              }
                              className={`rounded px-2.5 py-1 text-xs font-semibold transition ${
                                activeTab === 'formal'
                                  ? 'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-white font-bold'
                                  : 'text-slate-500 hover:text-slate-700 dark:text-slate-400'
                              }`}
                            >
                              1. Definición Formal
                            </button>
                            <button
                              onClick={() =>
                                setActiveTabByConcept((prev) => ({ ...prev, [concept.id]: 'simple' }))
                              }
                              className={`rounded px-2.5 py-1 text-xs font-semibold transition ${
                                activeTab === 'simple'
                                  ? 'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-white font-bold'
                                  : 'text-slate-500 hover:text-slate-700 dark:text-slate-400'
                              }`}
                            >
                              2. En Palabras Simples
                            </button>
                            <button
                              onClick={() =>
                                setActiveTabByConcept((prev) => ({ ...prev, [concept.id]: 'example' }))
                              }
                              className={`rounded px-2.5 py-1 text-xs font-semibold transition ${
                                activeTab === 'example'
                                  ? 'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-white font-bold'
                                  : 'text-slate-500 hover:text-slate-700 dark:text-slate-400'
                              }`}
                            >
                              3. Ejemplo
                            </button>
                          </div>

                          {/* Tab Content */}
                          <div className="mt-2.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                            {activeTab === 'formal' && (
                              <div className="rounded-lg bg-slate-50 p-3 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800">
                                <div className="font-semibold text-slate-900 dark:text-slate-100 mb-1 text-xs">
                                  Definición Matemática / Teórica:
                                </div>
                                <div className="overflow-x-auto">
                                  <MathText content={concept.definition} />
                                </div>
                                {concept.explanation && (
                                  <div className="mt-2 pt-2 border-t border-slate-200/60 text-xs text-slate-600 dark:border-slate-700/60 dark:text-slate-400 overflow-x-auto">
                                    <MathText content={concept.explanation} />
                                  </div>
                                )}
                              </div>
                            )}

                            {activeTab === 'simple' && (
                              <div className="rounded-lg bg-teal-50/50 p-3 text-teal-950 dark:bg-teal-950/20 dark:text-teal-200 border border-teal-100 dark:border-teal-900/40">
                                <div className="font-semibold mb-1 text-xs">
                                  Explicación Intuitiva:
                                </div>
                                <div className="overflow-x-auto">
                                  <MathText content={concept.simple_explanation || concept.explanation} />
                                </div>
                              </div>
                            )}

                            {activeTab === 'example' && (
                              <div className="rounded-lg bg-slate-900 p-3 text-emerald-400 font-mono text-xs overflow-x-auto">
                                <pre className="whitespace-pre-wrap">{concept.example}</pre>
                              </div>
                            )}
                          </div>
                        </div>

                        {/* Trampas de Examen / Confusiones Comunes */}
                        {concept.common_confusions && (
                          <div className="rounded-lg border border-amber-200 bg-amber-50/60 p-2.5 text-xs text-amber-900 dark:border-amber-900/40 dark:bg-amber-950/20 dark:text-amber-300">
                            <div className="flex items-center space-x-1 font-bold mb-0.5 text-[11px]">
                              <AlertCircle className="h-3 w-3 text-amber-600" />
                              <span>Trampa de Examen:</span>
                            </div>
                            <div className="overflow-x-auto">
                              <MathText content={concept.common_confusions} />
                            </div>
                          </div>
                        )}

                        {/* Actions & Feedback Bar */}
                        <div className="flex flex-wrap items-center justify-between gap-2 border-t border-slate-100 pt-2.5 dark:border-slate-800">
                          <div className="flex items-center space-x-1.5">
                            <button
                              onClick={() => handleFeedback(concept.id, 'entendido')}
                              className={`rounded px-2 py-1 text-[11px] font-semibold transition ${
                                feedback === 'dominado'
                                  ? 'bg-emerald-600 text-white'
                                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300'
                              }`}
                            >
                              ✓ Lo entendí
                            </button>
                            <button
                              onClick={() => handleFeedback(concept.id, 'practicar')}
                              className={`rounded px-2 py-1 text-[11px] font-semibold transition ${
                                feedback === 'debil'
                                  ? 'bg-rose-600 text-white'
                                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300'
                              }`}
                            >
                              ⚡ Repasar
                            </button>
                          </div>

                          <button
                            onClick={() => onNavigateToPractice(currentTopic.id, concept.id)}
                            className="inline-flex items-center space-x-1 text-[11px] font-semibold text-teal-600 hover:underline dark:text-teal-400"
                          >
                            <span>Practicar este concepto →</span>
                          </button>
                        </div>

                        {/* Personal Notes */}
                        <div className="pt-1.5 border-t border-dashed border-slate-200 dark:border-slate-800">
                          <div className="flex items-center justify-between text-[10px] text-slate-400 mb-1">
                            <span>Tus notas personales:</span>
                            {savedNotesMessage[concept.id] && (
                              <span className="text-emerald-600 font-bold">¡Guardado!</span>
                            )}
                          </div>
                          <div className="flex items-center space-x-1.5">
                            <input
                              type="text"
                              value={notesState[concept.id] || ''}
                              onChange={(e) =>
                                setNotesState((prev) => ({ ...prev, [concept.id]: e.target.value }))
                              }
                              placeholder="Escribí notas o recordatorios para este concepto..."
                              className="w-full rounded border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs text-slate-800 focus:outline-none focus:border-slate-400 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
                            />
                            <button
                              onClick={() => handleSaveNote(concept.id)}
                              className="rounded bg-slate-200 px-2.5 py-1 text-xs font-semibold text-slate-700 hover:bg-slate-300 dark:bg-slate-700 dark:text-slate-200 flex-shrink-0"
                            >
                              Guardar
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })
                ) : (
                  <div className="rounded-xl border border-slate-200 bg-white p-8 text-center text-xs text-slate-400">
                    No se encontraron conceptos para este tema.
                  </div>
                )}
              </div>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default TheoryPage;
