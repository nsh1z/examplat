import React from 'react';
import { Database, Flame, Zap, Sun, Moon, Search, Menu } from 'lucide-react';
import { DashboardData } from '../types';

interface NavbarProps {
  dashboard: DashboardData | null;
  darkMode: boolean;
  onToggleDarkMode: () => void;
  onOpenSearch: () => void;
  onOpenMobileMenu: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  dashboard,
  darkMode,
  onToggleDarkMode,
  onOpenSearch,
  onOpenMobileMenu
}) => {
  const user = dashboard?.user || {
    name: 'Estudiante',
    xp: 0,
    level: 1,
    streak_days: 1
  };

  return (
    <header className="sticky top-0 z-30 flex h-14 sm:h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-3 sm:px-6 backdrop-blur dark:border-slate-800 dark:bg-navy-900/95 transition-colors">
      {/* Left: Mobile burger + Brand */}
      <div className="flex items-center space-x-2 sm:space-x-3">
        <button
          onClick={onOpenMobileMenu}
          className="lg:hidden rounded-lg p-1.5 text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
          aria-label="Abrir menú de navegación"
        >
          <Menu className="h-5 w-5" />
        </button>

        <div className="flex items-center space-x-2.5">
          <div className="flex h-8 w-8 sm:h-9 sm:w-9 items-center justify-center rounded-lg bg-slate-900 text-white dark:bg-teal-600 shadow-sm flex-shrink-0">
            <Database className="h-4 w-4" />
          </div>
          <div>
            <h1 className="text-xs sm:text-sm font-bold tracking-tight text-slate-900 dark:text-white leading-tight">
              Ingeniería de Datos I
            </h1>
            <p className="hidden xs:block text-[10px] text-slate-500 dark:text-slate-400">
              Guía de Examen & Práctica
            </p>
          </div>
        </div>
      </div>

      {/* Right: Metrics & Controls */}
      <div className="flex items-center space-x-1.5 sm:space-x-3">
        {/* Search quick button */}
        <button
          onClick={onOpenSearch}
          className="flex items-center space-x-1.5 rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1.5 text-xs text-slate-600 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
          title="Buscar en apuntes y PDFs"
        >
          <Search className="h-3.5 w-3.5" />
          <span className="hidden md:inline text-[11px]">Buscar...</span>
        </button>

        {/* Streak */}
        <div
          className="flex items-center space-x-1 rounded-lg bg-amber-50 px-2 py-1 text-xs font-semibold text-amber-700 border border-amber-200 dark:bg-amber-950/40 dark:border-amber-900/50 dark:text-amber-400"
          title="Racha de estudio diario"
        >
          <Flame className="h-3.5 w-3.5 text-amber-500 fill-amber-500" />
          <span className="text-[11px]">{user.streak_days}d</span>
        </div>

        {/* Level / XP */}
        <div
          className="hidden sm:flex items-center space-x-1 rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-700 dark:bg-slate-800 dark:text-slate-300"
          title="Nivel y experiencia acumulada"
        >
          <span>Nv.{user.level}</span>
          <span className="text-slate-300 dark:text-slate-600">|</span>
          <Zap className="h-3 w-3 text-amber-500 fill-amber-500" />
          <span className="text-[11px]">{user.xp} XP</span>
        </div>

        {/* Dark Mode Toggle */}
        <button
          onClick={onToggleDarkMode}
          className="rounded-lg p-1.5 text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800"
          title={darkMode ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
          aria-label="Cambiar tema"
        >
          {darkMode ? (
            <Sun className="h-4 w-4 text-amber-400" />
          ) : (
            <Moon className="h-4 w-4 text-slate-600" />
          )}
        </button>
      </div>
    </header>
  );
};

export default Navbar;
