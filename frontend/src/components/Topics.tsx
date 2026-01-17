import { useQuery } from '@tanstack/react-query';
import { topicsAPI } from '@/services/api';

export function Topics() {
  const { data: topics, isLoading } = useQuery({
    queryKey: ['topics'],
    queryFn: async () => (await topicsAPI.getAll()).data,
  });

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-2">Audit Finding Themes</h2>
        <p className="text-gray-600 mb-6">
          25 audit finding topics identified through LDA topic modeling (k=25) of Philippine COA reports (2010-2020)
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {topics?.map((topic) => (
            <div
              key={topic.id}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-primary-100 text-primary-700 text-sm font-semibold">
                      {topic.topic_number}
                    </span>
                    <h3 className="font-semibold text-gray-900">{topic.description}</h3>
                  </div>
                  {topic.terms && (
                    <p className="text-sm text-gray-500 mt-2">
                      <span className="font-medium">Key terms:</span> {topic.terms.substring(0, 100)}...
                    </p>
                  )}
                  {topic.prevalence && (
                    <div className="mt-3">
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-primary-600 h-2 rounded-full"
                            style={{ width: `${Number(topic.prevalence) * 100}%` }}
                          />
                        </div>
                        <span className="text-xs text-gray-600 font-medium">
                          {(Number(topic.prevalence) * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">About These Topics</h3>
        <p className="text-blue-800 text-sm">
          These 25 topics were automatically identified through Latent Dirichlet Allocation (LDA) topic modeling
          of audit findings sections from 17,392 executive summaries spanning Philippine local governments
          from 2010 to 2020. Each topic represents a cluster of related audit issues frequently mentioned
          across different municipalities and cities.
        </p>
      </div>
    </div>
  );
}
