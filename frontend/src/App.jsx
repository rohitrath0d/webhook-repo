import React, { useEffect, useState } from 'react';
import api from './services/api';
import Filters from './components/Filters';
import Events from './components/Events';

const App = () => {
  const [events, setEvents] = useState([]);
  const [filter, setFilter] = useState('ALL');

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await api.get('/webhook/events');
        console.log("event data response ---------->", response.data);
        // console.log("event data response ---------->", response.data.events);
        
        setEvents(Array.isArray(response.data) ? response.data : []);

      } catch (error) {
        console.error('Error fetching events:', error);
        setEvents([]);
      }
    };

    fetchEvents();
    const interval = setInterval(fetchEvents, 15000);     // fetching / polling every 15 seconds
    return () => clearInterval(interval);
  }, []);

  const filteredEvents = events.filter(
    (event) => filter === 'ALL' || event.action === filter
  );

  return (
    <div className="min-h-screen pb-12 bg-[#12121a] text-gray-100">
      <header className="bg-[#1a1a24] border-b border-white/10 py-6 px-8 text-center">
        <h1 className="text-2xl font-bold text-violet-400">GitHub Activity</h1>
        <p className="mt-2 text-gray-400 text-sm">Real-time event stream</p>
      </header>
      <main className="max-w-[500px] mx-auto py-8 px-4">
        <Filters filter={filter} setFilter={setFilter} />
        <Events events={filteredEvents} />
      </main>
    </div>
  );
};

export default App;
