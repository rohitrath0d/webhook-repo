import React from 'react';

const filters = [
  { key: 'ALL', label: 'All', icon: '📋' },
  { key: 'PUSH', label: 'Push', icon: '↑' },
  { key: 'PULL_REQUEST', label: 'Pull Request', icon: '⤴' },
  { key: 'MERGE', label: 'Merge', icon: '⤵' },
];

const Filters = ({ filter, setFilter }) => (
  <div className="flex justify-center gap-2 mb-8 flex-wrap">
    {filters.map(({ key, label, icon }) => (
      <button
        key={key}
        className={`flex items-center gap-2 px-4 py-2 border rounded-full text-sm font-medium cursor-pointer transition-all duration-200
          ${filter === key
            ? 'bg-indigo-500 border-transparent text-white'
            : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:border-white/20 hover:text-white'
          }`}
        onClick={() => setFilter(key)}
      >
        <span>{icon}</span>
        {label}
      </button>
    ))}
  </div>
);

export default Filters;
