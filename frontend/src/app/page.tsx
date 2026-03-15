'use client';
import { useState } from 'react';
import Header from "@/components/Header";
import InputForm from "@/components/InputForm";
import Arena from "@/components/Arena";
import { MOCK_STREAM } from "@/lib/mockStream";

export default function Home() {
  const [messages, setMessages] = useState<any[]>([]);
  const [status, setStatus] = useState<'idle' | 'loading' | 'streaming'>('idle');

  const startRoast = (url: string) => {
    setStatus('loading');
    
    // Switch between DEMO mode and REAL API mode
    const isDemo = true; // CHANGE THIS TO 'false' WHEN DAVIN GIVES YOU THE URL

    if (isDemo) {
      setTimeout(() => setStatus('streaming'), 2000);
      MOCK_STREAM.forEach((item, index) => {
        setTimeout(() => {
          setMessages((prev) => [...prev, item]);
        }, 2000 + (index * 1500));
      });
    } else {
      // REAL API CALL
      const eventSource = new EventSource(`YOUR_RAILWAY_URL/analyze?url=${encodeURIComponent(url)}`);
      setStatus('streaming');
      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setMessages((prev) => [...prev, data]);
      };
    }
  };

  return (
    <main className="min-h-screen bg-black text-white">
      <Header />
      {status === 'idle' && <InputForm onRoast={startRoast} />}
      {status === 'loading' && <div className="text-center mt-20 animate-pulse">Analyzing Repository...</div>}
      {status === 'streaming' && <Arena messages={messages} />}
    </main>
  );
}