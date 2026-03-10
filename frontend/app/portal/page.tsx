'use client';

import { useEffect, useMemo, useState } from 'react';

export default function PortalPage() {
  const hotelSlug = useMemo(() => new URLSearchParams(typeof window !== 'undefined' ? window.location.search : '').get('hotel') || 'demo-hotel', []);
  const [branding, setBranding] = useState<any>(null);
  const [roomNumber, setRoomNumber] = useState('');
  const [lastName, setLastName] = useState('');
  const [voucherCode, setVoucherCode] = useState('');
  const [mode, setMode] = useState<'room' | 'voucher'>('room');
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'}/api/hotels/${hotelSlug}/branding`).then(r => r.json()).then(setBranding).catch(() => undefined);
  }, [hotelSlug]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const body = mode === 'room'
      ? { hotel_slug: hotelSlug, room_number: roomNumber, last_name: lastName }
      : { hotel_slug: hotelSlug, voucher_code: voucherCode };
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'}/api/portal/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    setMessage(res.ok ? 'Connected. Redirect to MikroTik login success URL here.' : 'Login failed.');
  }

  return (
    <main style={{ minHeight: '100vh', display: 'grid', placeItems: 'center', padding: 20 }}>
      <div style={{ width: '100%', maxWidth: 420, background: '#fff', borderRadius: 16, padding: 24, boxShadow: '0 10px 30px rgba(0,0,0,0.08)' }}>
        {branding?.logo_url ? <img src={branding.logo_url} alt="logo" style={{ maxHeight: 64, marginBottom: 12 }} /> : null}
        <h1 style={{ margin: 0 }}>{branding?.name || 'Hotel WiFi'}</h1>
        <p>{branding?.welcome_message || 'Welcome. Please sign in to access the internet.'}</p>
        <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
          <button onClick={() => setMode('room')}>Room + Last Name</button>
          <button onClick={() => setMode('voucher')}>Voucher</button>
        </div>
        <form onSubmit={submit} style={{ display: 'grid', gap: 12 }}>
          {mode === 'room' ? (
            <>
              <input value={roomNumber} onChange={e => setRoomNumber(e.target.value)} placeholder="Room Number" />
              <input value={lastName} onChange={e => setLastName(e.target.value)} placeholder="Last Name" />
            </>
          ) : (
            <input value={voucherCode} onChange={e => setVoucherCode(e.target.value)} placeholder="Voucher Code" />
          )}
          <button type="submit">Connect</button>
        </form>
        {message ? <p>{message}</p> : null}
      </div>
    </main>
  );
}
