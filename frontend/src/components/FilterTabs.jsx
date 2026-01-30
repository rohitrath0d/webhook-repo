import React from 'react';

const FilterTabs = ({ filter, setFilter }) => {
  const tabs = ['ALL', 'PUSH', 'PULL_REQUEST', 'MERGE'];

  return (
    <div className="flex justify-center space-x-4 my-4">
      {tabs.map((type) => (
        <button
          key={type}
          className={`px-4 py-2 rounded-md font-medium transition-colors duration-200 ${
            filter === type
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
          }`}
          onClick={() => setFilter(type)}
        >
          {type}
        </button>
      ))}
    </div>
  );
};

export default FilterTabs;