import React from 'react';

const EventItem = ({ event }) => {
  const formatEvent = () => {
    switch (event.action) {
      case 'PUSH':
        return `${event.author} pushed to ${event.to_branch} on ${new Date(event.timestamp).toUTCString()}`;
      case 'PULL_REQUEST':
        return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${new Date(event.timestamp).toUTCString()}`;
      case 'MERGE':
        return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${new Date(event.timestamp).toUTCString()}`;
      default:
        return 'Unknown event';
    }
  };

  return <li>{formatEvent()}</li>;
};

export default EventItem;