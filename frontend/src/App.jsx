import React, { useEffect, useState } from 'react';
import api from './services/api';
import FilterTabs from './components/FilterTabs';
import EventList from './components/EventList';

const App = () => {
  const [events, setEvents] = useState([]);
  const [filter, setFilter] = useState('ALL');

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await api.get('/events');
        setEvents(response.data);
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    };

    fetchEvents();
    const interval = setInterval(fetchEvents, 15000);
    return () => clearInterval(interval);
  }, []);

  const filteredEvents = events.filter(
    (event) => filter === 'ALL' || event.action === filter
  );

  return (
    <div className="min-h-screen bg-gray-100 text-gray-800">
      <header className="bg-blue-600 text-white py-4 shadow-md">
        <h1 className="text-center text-2xl font-bold">GitHub Events</h1>
      </header>
      <main className="max-w-4xl mx-auto py-6 px-4">
        <FilterTabs filter={filter} setFilter={setFilter} />
        <EventList events={filteredEvents} />
      </main>
    </div>
  );
};

export default App;
