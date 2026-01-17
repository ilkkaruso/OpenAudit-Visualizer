import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { transactionsAPI, lgusAPI } from '@/services/api';
import type { UnliquidatedTransaction } from '@/types';

export function Explorer() {
  const [selectedYear, setSelectedYear] = useState<number | undefined>();
  const [selectedProvince, setSelectedProvince] = useState<string | undefined>();
  const [minAmount, setMinAmount] = useState<number | undefined>();
  const [maxAmount, setMaxAmount] = useState<number | undefined>();

  const { data: years } = useQuery({
    queryKey: ['years'],
    queryFn: async () => (await transactionsAPI.getYears()).data,
  });

  const { data: provinces } = useQuery({
    queryKey: ['provinces'],
    queryFn: async () => (await lgusAPI.getProvinces()).data,
  });

  const { data: transactions, isLoading } = useQuery({
    queryKey: ['transactions', selectedYear, selectedProvince, minAmount, maxAmount],
    queryFn: async () =>
      (await transactionsAPI.getAll({
        year: selectedYear,
        province: selectedProvince,
        min_amount: minAmount,
        max_amount: maxAmount,
        limit: 100,
      })).data,
  });

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-4">Data Explorer</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Year</label>
            <select
              value={selectedYear || ''}
              onChange={(e) => setSelectedYear(e.target.value ? Number(e.target.value) : undefined)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All Years</option>
              {years?.map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Province</label>
            <select
              value={selectedProvince || ''}
              onChange={(e) => setSelectedProvince(e.target.value || undefined)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All Provinces</option>
              {provinces?.map((province) => (
                <option key={province} value={province}>
                  {province}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Min Amount</label>
            <input
              type="number"
              value={minAmount || ''}
              onChange={(e) => setMinAmount(e.target.value ? Number(e.target.value) : undefined)}
              placeholder="Min"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Max Amount</label>
            <input
              type="number"
              value={maxAmount || ''}
              onChange={(e) => setMaxAmount(e.target.value ? Number(e.target.value) : undefined)}
              placeholder="Max"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>

        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">LGU</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Province</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Year</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {transactions?.map((transaction) => (
                  <tr key={transaction.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {transaction.lgu?.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {transaction.lgu?.province}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{transaction.year}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                      ₱{transaction.amount.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {transactions && transactions.length === 0 && (
              <div className="text-center py-12 text-gray-500">No transactions found</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
