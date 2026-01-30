import React from 'react';

const FilterTabs = ({ filter, setFilter }) => {
  const tabs = ['ALL', 'PUSH', 'PULL_REQUEST', 'MERGE'];

  return (
    <div className="tabs">
      {tabs.map((type) => (
        <button
          key={type}
          className={filter === type ? 'active' : ''}
          onClick={() => setFilter(type)}
        >
          {type}
        </button>
      ))}
    </div>
  );
};

export default FilterTabs;