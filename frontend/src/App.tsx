import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Dashboard } from './components/Dashboard';
import { Explorer } from './components/Explorer';
import { Topics } from './components/Topics';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

type Tab = 'dashboard' | 'explorer' | 'topics';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('dashboard');

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">OpenAudit Visualizer</h1>
                <p className="text-sm text-gray-600 mt-1">
                  Philippine Audit Reports Data Explorer (2010-2020)
                </p>
              </div>
            </div>

            <nav className="flex space-x-8 -mb-px">
              <TabButton
                label="Dashboard"
                icon="📊"
                active={activeTab === 'dashboard'}
                onClick={() => setActiveTab('dashboard')}
              />
              <TabButton
                label="Data Explorer"
                icon="🔍"
                active={activeTab === 'explorer'}
                onClick={() => setActiveTab('explorer')}
              />
              <TabButton
                label="Audit Topics"
                icon="📑"
                active={activeTab === 'topics'}
                onClick={() => setActiveTab('topics')}
              />
            </nav>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {activeTab === 'dashboard' && <Dashboard />}
          {activeTab === 'explorer' && <Explorer />}
          {activeTab === 'topics' && <Topics />}
        </main>

        <footer className="bg-white border-t border-gray-200 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <p className="text-sm text-gray-500 text-center">
              OpenAudit: Advancing governance research with NLP-processed audit reports
            </p>
            <p className="text-xs text-gray-400 text-center mt-2">
              Data source: Philippine Commission on Audit (COA) | MIT GOV/LAB
            </p>
          </div>
        </footer>
      </div>
    </QueryClientProvider>
  );
}

interface TabButtonProps {
  label: string;
  icon: string;
  active: boolean;
  onClick: () => void;
}

function TabButton({ label, icon, active, onClick }: TabButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-4 border-b-2 font-medium text-sm transition-colors ${
        active
          ? 'border-primary-600 text-primary-600'
          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
      }`}
    >
      <span>{icon}</span>
      <span>{label}</span>
    </button>
  );
}

export default App;
