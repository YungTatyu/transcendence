
'use client';

import React, { createContext, useContext, useState } from 'react';

const UsernameContext = createContext(null);

// Providerコンポーネント
export function UsernameProvider({ children }) {
  const [username, setUsername] = useState('');

  return (
    <UsernameContext.Provider value={{ username, setUsername }}>
      {children}
    </UsernameContext.Provider>
  );
}

export function useUsername() {
  const context = useContext(UsernameContext);
  if (!context) {
    throw new Error('useUsername must be used within a UsernameProvider');
  }
  return context;
}
