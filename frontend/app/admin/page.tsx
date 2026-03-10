'use client';

import { useEffect, useState } from 'react';

export default function AdminPage() {
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;
    fetch(`${process.env.NEXT_PUBLIC_API_BASE || '/api'}/api/dashboard/summary`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json())
      .then(setSummary)
      .catch(() => undefined);
  }, []);

  return (
    <main style={{ padding: 32 }}>
      <h1>Admin Dashboard</h1>
      <div style={{ display: 'grid', gap: 16, gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))' }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 14 }}>
          <h3>Active Guests</h3>
          <strong>{summary?.active_guests ?? '-'}</strong>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 14 }}>
          <h3>Online Sessions</h3>
          <strong>{summary?.online_sessions ?? '-'}</strong>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 14 }}>
          <h3>Bandwidth Used</h3>
          <strong>{summary?.bandwidth_bytes ?? '-'}</strong>
        </div>
      </div>
    </main>
  );
}
