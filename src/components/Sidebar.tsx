import React from 'react';
import {
  LayoutDashboard,
  BookOpen,
  BrainCircuit,
  Database,
  GraduationCap,
  AlertCircle,
  Search,
  ShieldCheck,
  X,
  FileDown
} from 'lucide-react';

export type NavTab =
  | 'dashboard'
  | 'theory'
  | 'practice'
  | 'cases'
  | 'exam'
  | 'errors'
  | 'search'
  | 'admin';

interface SidebarProps {
  currentTab: NavTab;
  onSelectTab: (tab: NavTab) => void;
  weakCount?: number;
  mobileOpen: boolean;
  onCloseMobile: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  onSelectTab,
  weakCount = 0,
  mobileOpen,
  onCloseMobile
}) => {
  const items: Array<{ id: NavTab; label: string; icon: React.ReactNode; badge?: number }> = [
    {
      id: 'dashboard',
      label: 'Panel de Estudio',
      icon: <LayoutDashboard className="h-4 w-4" />
    },
    {
      id: 'theory',
      label: 'Teoría (6 Unidades)',
      icon: <BookOpen className="h-4 w-4" />
    },
    {
      id: 'practice',
      label: 'Práctica Adaptativa',
      icon: <BrainCircuit className="h-4 w-4" />
    },
    {
      id: 'cases',
      label: 'Casos & Álgebra',
      icon: <Database className="h-4 w-4" />
    },
    {
      id: 'exam',
      label: 'Simulador Examen',
      icon: <GraduationCap className="h-4 w-4" />
    },
    {
      id: 'errors',
      label: 'Mis Errores',
      icon: <AlertCircle className="h-4 w-4" />,
      badge: weakCount > 0 ? weakCount : undefined
    },
    {
      id: 'search',
      label: 'Buscar o Comparar',
      icon: <Search className="h-4 w-4" />
    },
    {
      id: 'admin',
      label: 'Auditoría de Temas',
      icon: <ShieldCheck className="h-4 w-4" />
    }
  ];

  const handleSelect = (id: NavTab) => {
    onSelectTab(id);
    onCloseMobile();
  };

  const navContent = (
    <div className="flex h-full flex-col justify-between p-3 select-none">
      <div className="space-y-1">
        <div className="px-3 pb-2 pt-1 text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
          Módulos de Estudio
        </div>
        {items.map((item) => {
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => handleSelect(item.id)}
              className={`flex w-full items-center justify-between rounded-lg px-3 py-2 text-xs font-medium transition-colors ${
                isActive
                  ? 'bg-slate-900 text-white dark:bg-teal-600 dark:text-white font-semibold shadow-sm'
                  : 'text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800'
              }`}
            >
              <div className="flex items-center space-x-2.5">
                <span className={isActive ? 'text-white' : 'text-slate-400 dark:text-slate-400'}>
                  {item.icon}
                </span>
                <span>{item.label}</span>
              </div>
              {item.badge !== undefined && (
                <span className="rounded-full bg-rose-100 px-1.5 py-0.5 text-[10px] font-bold text-rose-700 dark:bg-rose-950 dark:text-rose-400">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Footer Info */}
      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-[11px] text-slate-500 dark:border-slate-800 dark:bg-slate-800/60 dark:text-slate-400">
        <div className="font-semibold text-slate-700 dark:text-slate-200">
          Ingeniería de Datos I
        </div>
        <div className="mt-0.5 text-[10px]">
          Temario Oficial: 5 Documentos de Cátedra
        </div>
        <a
          href="/Material_de_Estudio_Ingenieria_de_Datos_I.pdf"
          download
          className="mt-2.5 flex items-center justify-center space-x-1.5 rounded-lg border border-teal-200 bg-teal-50 px-2.5 py-1.5 text-[11px] font-bold text-teal-700 hover:bg-teal-100 dark:border-teal-900/60 dark:bg-teal-950/40 dark:text-teal-300 transition-colors"
        >
          <FileDown className="h-3.5 w-3.5" />
          <span>Descargar Apunte PDF</span>
        </a>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar (hidden on mobile/tablet < 1024px) */}
      <aside className="hidden lg:flex w-60 flex-shrink-0 border-r border-slate-200 bg-white dark:border-slate-800 dark:bg-navy-900">
        {navContent}
      </aside>

      {/* Mobile Drawer (Visible when mobileOpen is true on small screens) */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-black/40 backdrop-blur-sm transition-opacity"
            onClick={onCloseMobile}
          />

          {/* Drawer Content */}
          <div className="fixed inset-y-0 left-0 w-72 max-w-[80vw] bg-white dark:bg-navy-900 shadow-2xl border-r border-slate-200 dark:border-slate-800 flex flex-col z-10 animate-in slide-in-from-left duration-200">
            <div className="flex items-center justify-between border-b border-slate-100 px-4 py-3 dark:border-slate-800">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-600 dark:text-slate-300">
                Navegación
              </span>
              <button
                onClick={onCloseMobile}
                className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600 dark:hover:bg-slate-800 dark:hover:text-slate-200"
                aria-label="Cerrar menú"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto">
              {navContent}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Sidebar;
