import React, { useEffect, useState } from 'react';
import api from './services/api';
import FilterTabs from './components/FilterTabs';
import EventList from './components/EventList';
import './App.css';

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
    <div className="App">
      <h1>GitHub Events</h1>
      <FilterTabs filter={filter} setFilter={setFilter} />
      <EventList events={filteredEvents} />
    </div>
  );
};

export default App;
