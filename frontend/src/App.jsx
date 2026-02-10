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

    console.log("[POLLING STARTED]: <------------- initializing polling");

    fetchEvents();

    const interval = setInterval(fetchEvents, 15000);     // fetching / polling every 15 seconds
    console.log("[POLLING ENDED]: <---------------- ending polling");
    return () => clearInterval(interval);

  }, []);

  const filteredEvents = events.filter(
    (event) => filter === 'ALL' || event.action === filter
  );

  return (
    <div className="min-h-screen pb-12 bg-gray-300 text-gray-100">
      <header className="bg-gray-300 py-4 px-8 text-center">
        <h1 className="text-2xl font-bold text-black">GitHub Repo Actions</h1>
      </header>
      <main className="max-w-[600px] mx-auto py-4 px-4">
        <Filters filter={filter} setFilter={setFilter} />
        <Events events={filteredEvents} />
      </main>
    </div>
  );
};

export default App;
