import { useQuery } from '@tanstack/react-query';
import { analyticsAPI, transactionsAPI } from '@/services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

export function Dashboard() {
  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: async () => (await analyticsAPI.getStats()).data,
  });

  const { data: yearlyTrends } = useQuery({
    queryKey: ['yearlyTrends'],
    queryFn: async () => (await analyticsAPI.getYearlyTrends()).data,
  });

  const { data: topLGUs } = useQuery({
    queryKey: ['topLGUs'],
    queryFn: async () => (await transactionsAPI.getTopLGUs(10)).data,
  });

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total LGUs"
          value={stats?.total_lgus.toLocaleString() || '-'}
          icon="🏛️"
        />
        <StatCard
          title="Total Reports"
          value={stats?.total_reports.toLocaleString() || '-'}
          icon="📄"
        />
        <StatCard
          title="Provinces Covered"
          value={stats?.provinces_count.toLocaleString() || '-'}
          icon="📍"
        />
        <StatCard
          title="Total Unliquidated"
          value={`₱${(stats?.total_unliquidated_amount / 1000000).toFixed(1)}M` || '-'}
          icon="💰"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Yearly Trends</h3>
          {yearlyTrends && (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={yearlyTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip formatter={(value) => `₱${Number(value).toLocaleString()}`} />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="total_amount"
                  stroke="#0ea5e9"
                  name="Total Amount"
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Top 10 LGUs by Unliquidated Amount</h3>
          {topLGUs && (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topLGUs.slice(0, 10)} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="lgu_name" type="category" width={100} />
                <Tooltip formatter={(value) => `₱${Number(value).toLocaleString()}`} />
                <Bar dataKey="total_amount" fill="#0ea5e9" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Top LGUs Details</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">LGU</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Province</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Amount</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Transactions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {topLGUs?.slice(0, 20).map((lgu) => (
                <tr key={lgu.lgu_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {lgu.lgu_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{lgu.province}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ₱{lgu.total_amount.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {lgu.transaction_count}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: string;
  icon: string;
}

function StatCard({ title, value, icon }: StatCardProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900 mt-2">{value}</p>
        </div>
        <div className="text-4xl">{icon}</div>
      </div>
    </div>
  );
}
