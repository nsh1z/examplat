import React from 'react';
import {
  LayoutDashboard,
  BookOpen,
  BrainCircuit,
  GraduationCap,
  Menu
} from 'lucide-react';
import { NavTab } from './Sidebar';

interface MobileNavProps {
  currentTab: NavTab;
  onSelectTab: (tab: NavTab) => void;
  onOpenDrawer: () => void;
  weakCount?: number;
}

export const MobileNav: React.FC<MobileNavProps> = ({
  currentTab,
  onSelectTab,
  onOpenDrawer,
  weakCount = 0
}) => {
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 lg:hidden border-t border-slate-200 bg-white/95 backdrop-blur dark:border-slate-800 dark:bg-navy-900/95 safe-bottom">
      <div className="flex h-14 items-center justify-around px-2">
        {/* 1. Dashboard */}
        <button
          onClick={() => onSelectTab('dashboard')}
          className={`flex flex-col items-center justify-center flex-1 py-1 text-[10px] font-medium transition-colors ${
            currentTab === 'dashboard'
              ? 'text-teal-600 dark:text-teal-400 font-bold'
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-700'
          }`}
        >
          <LayoutDashboard className="h-4 w-4 mb-0.5" />
          <span>Inicio</span>
        </button>

        {/* 2. Theory */}
        <button
          onClick={() => onSelectTab('theory')}
          className={`flex flex-col items-center justify-center flex-1 py-1 text-[10px] font-medium transition-colors ${
            currentTab === 'theory'
              ? 'text-teal-600 dark:text-teal-400 font-bold'
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-700'
          }`}
        >
          <BookOpen className="h-4 w-4 mb-0.5" />
          <span>Teoría</span>
        </button>

        {/* 3. Practice */}
        <button
          onClick={() => onSelectTab('practice')}
          className={`flex flex-col items-center justify-center flex-1 py-1 text-[10px] font-medium transition-colors ${
            currentTab === 'practice'
              ? 'text-teal-600 dark:text-teal-400 font-bold'
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-700'
          }`}
        >
          <BrainCircuit className="h-4 w-4 mb-0.5" />
          <span>Práctica</span>
        </button>

        {/* 4. Exam */}
        <button
          onClick={() => onSelectTab('exam')}
          className={`flex flex-col items-center justify-center flex-1 py-1 text-[10px] font-medium transition-colors ${
            currentTab === 'exam'
              ? 'text-teal-600 dark:text-teal-400 font-bold'
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-700'
          }`}
        >
          <GraduationCap className="h-4 w-4 mb-0.5" />
          <span>Examen</span>
        </button>

        {/* 5. More / Drawer Trigger */}
        <button
          onClick={onOpenDrawer}
          className="relative flex flex-col items-center justify-center flex-1 py-1 text-[10px] font-medium text-slate-500 dark:text-slate-400 hover:text-slate-700 transition-colors"
        >
          <Menu className="h-4 w-4 mb-0.5" />
          <span>Más</span>
          {weakCount > 0 && (
            <span className="absolute top-1 right-3 h-2 w-2 rounded-full bg-rose-500" />
          )}
        </button>
      </div>
    </nav>
  );
};

export default MobileNav;
