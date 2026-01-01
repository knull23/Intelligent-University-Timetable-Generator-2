import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface FitnessProgressionChartProps {
  data: number[];
  title?: string;
}

const FitnessProgressionChart: React.FC<FitnessProgressionChartProps> = ({
  data,
  title = "Fitness Progression Over Generations"
}) => {
  // Transform the data array into the format expected by Recharts
  const chartData = data.map((fitness, index) => ({
    generation: index + 1,
    fitness: fitness
  }));

  return (
    <div className="w-full h-96 bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">{title}</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={chartData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="generation"
            label={{ value: 'Generation', position: 'insideBottom', offset: -5 }}
          />
          <YAxis
            label={{ value: 'Fitness Score (%)', angle: -90, position: 'insideLeft' }}
            domain={[0, 100]}
          />
          <Tooltip
            formatter={(value: number) => [`${value.toFixed(2)}%`, 'Fitness']}
            labelFormatter={(label) => `Generation ${label}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="fitness"
            stroke="#2563eb"
            strokeWidth={2}
            dot={{ fill: '#2563eb', strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6 }}
            name="Fitness Score"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default FitnessProgressionChart;
