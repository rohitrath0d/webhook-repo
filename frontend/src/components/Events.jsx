import React from 'react';

const actionConfig = {
  PUSH: { label: 'pushed to', color: 'bg-orange-100', icon: '↑' },
  PULL_REQUEST: { label: 'opened PR', color: 'bg-slate-300', icon: '⤴' },
  MERGE: { label: 'merged', color: 'bg-emerald-300', icon: '⤵' },
};

const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  const weekday = date.toLocaleDateString('en-US', { weekday: 'long' });
  const day = date.getDate();
  const month = date.toLocaleDateString('en-US', { month: 'short' });
  const year = date.getFullYear();
  const time = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  return `${weekday}, ${day} ${month} ${year} • ${time}`;
};

const EventCard = ({ event }) => {
  const config = actionConfig[event.action] || { label: 'did something', color: 'bg-gray-500', icon: '?' };

  return (
    <div className="relative bg-slate-800/70 border border-white/10 rounded-xl px-4 py-3 backdrop-blur-sm transition-all duration-300 hover:-translate-y-0.5 hover:border-indigo-400/30 hover:shadow-lg">
      <div className="flex items-center flex-wrap gap-1.5">
        <span className="font-bold text-white">{event.author}</span>
        <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold text-black lowercase ${config.color}`}>
          {config.icon} {config.label}
        </span>

        {event.action === 'PUSH' && (
          <span className="inline-flex items-center gap-1 text-gray-400 text-sm">
            <span className="bg-white/10 px-2 py-0.5 rounded text-white font-mono text-xs">{event.to_branch}</span>
          </span>
        )}

        {(event.action === 'PULL_REQUEST' || event.action === 'MERGE') && (
          <span className="inline-flex items-center gap-1 text-white text-sm">
            <span className="bg-white/10 px-2 py-0.5 rounded text-white font-mono text-xs">{event.from_branch}</span>
            <span className="opacity-60">→</span>
            <span className="bg-white/10 px-2 py-0.5 rounded text-white font-mono text-xs">{event.to_branch}</span>
          </span>
        )}

        <span className="text-xs text-white ml-auto whitespace-nowrap">{formatTime(event.timestamp)}</span>
      </div>
    </div>
  );
};

const Events = ({ events }) => {
  if (!events.length) {
    return (
      <div className="text-center py-16 text-gray-400">
        <p className='text-3xl mb-4'>No events yet</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2.5">
      {events.map((event) => (
        <EventCard key={event._id} event={event} />
      ))}
    </div>
  );
};

export default Events;
