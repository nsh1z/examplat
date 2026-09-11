import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar, { NavTab } from './components/Sidebar';
import MobileNav from './components/MobileNav';
import DashboardPage from './pages/DashboardPage';
import TheoryPage from './pages/TheoryPage';
import PracticePage from './pages/PracticePage';
import CasesPage from './pages/CasesPage';
import ExamPage from './pages/ExamPage';
import ErrorsPage from './pages/ErrorsPage';
import SearchPage from './pages/SearchPage';
import AdminPage from './pages/AdminPage';
import { fetchDashboard } from './api';
import { DashboardData } from './types';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<NavTab>('dashboard');
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState<boolean>(false);

  // Navigation params for cross-page jumping
  const [navParams, setNavParams] = useState<{
    unitNumber?: number;
    topicId?: string;
    conceptId?: string;
  }>({});

  // Dark mode state
  const [darkMode, setDarkMode] = useState<boolean>(() => {
    const saved = localStorage.getItem('theme');
    if (saved) return saved === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  // Load dashboard data
  const loadDashboard = async () => {
    try {
      const data = await fetchDashboard();
      setDashboardData(data);
    } catch (err) {
      console.error('Error al cargar dashboard', err);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const handleNavigate = (tab: NavTab, params?: any) => {
    if (params) {
      setNavParams(params);
    } else {
      setNavParams({});
    }
    setCurrentTab(tab);
    setMobileDrawerOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 dark:bg-navy-950 dark:text-slate-100 flex flex-col font-sans transition-colors duration-200">
      {/* Top Navigation Bar */}
      <Navbar
        dashboard={dashboardData}
        darkMode={darkMode}
        onToggleDarkMode={() => setDarkMode(!darkMode)}
        onOpenSearch={() => handleNavigate('search')}
        onOpenMobileMenu={() => setMobileDrawerOpen(true)}
      />

      {/* Main Content Area: Sidebar + Active Page */}
      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          currentTab={currentTab}
          onSelectTab={(tab) => handleNavigate(tab)}
          weakCount={dashboardData?.stats?.debiles || 0}
          mobileOpen={mobileDrawerOpen}
          onCloseMobile={() => setMobileDrawerOpen(false)}
        />

        <main className="flex-1 overflow-y-auto px-3 sm:px-8 py-5 pb-20 lg:pb-6 max-w-7xl mx-auto w-full">
          {currentTab === 'dashboard' && (
            <DashboardPage
              data={dashboardData}
              onNavigate={handleNavigate}
              onRefresh={loadDashboard}
            />
          )}

          {currentTab === 'theory' && (
            <TheoryPage
              initialUnitNumber={navParams.unitNumber}
              initialConceptId={navParams.conceptId}
              onNavigateToPractice={(topicId, conceptId) =>
                handleNavigate('practice', { topicId, conceptId })
              }
            />
          )}

          {currentTab === 'practice' && (
            <PracticePage
              initialTopicId={navParams.topicId}
              onRefreshDashboard={loadDashboard}
            />
          )}

          {currentTab === 'cases' && <CasesPage />}

          {currentTab === 'exam' && (
            <ExamPage
              onNavigateToPractice={(topicId) => handleNavigate('practice', { topicId })}
              onRefreshDashboard={loadDashboard}
            />
          )}

          {currentTab === 'errors' && (
            <ErrorsPage
              onNavigateToPractice={(topicId) => handleNavigate('practice', { topicId })}
              onRefreshDashboard={loadDashboard}
            />
          )}

          {currentTab === 'search' && (
            <SearchPage
              onNavigateToTheory={(topicId, conceptId) =>
                handleNavigate('theory', { topicId, conceptId })
              }
            />
          )}

          {currentTab === 'admin' && <AdminPage />}
        </main>
      </div>

      {/* Mobile Bottom Navigation Bar */}
      <MobileNav
        currentTab={currentTab}
        onSelectTab={(tab) => handleNavigate(tab)}
        onOpenDrawer={() => setMobileDrawerOpen(true)}
        weakCount={dashboardData?.stats?.debiles || 0}
      />
    </div>
  );
};

export default App;
