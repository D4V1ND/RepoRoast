'use client';
import { useState } from 'react';
import Header from "@/components/Header";
import InputForm from "@/components/InputForm";
import Arena from "@/components/Arena";
import { MOCK_STREAM } from "@/lib/mockStream";

const transformBackendData = (data: any): any[] => {
  const messages: any[] = [];

  if (data.node === "final_result") {
    const { output_alex, output_sam, output_jordan } = data;

    if (output_alex) {
      messages.push({ judge: "Alex", message: `Innovation Score: ${output_alex.innovation_score}/10` });
      messages.push({ judge: "Alex", message: `💡 Strongest Innovation: ${output_alex.strongest_innovation}` });
      output_alex.brutally_honest_feedback.forEach((f: string) => {
        messages.push({ judge: "Alex", message: f });
      });
    }

    if (output_sam) {
      messages.push({ judge: "Sam", message: `Architecture Score: ${output_sam.score}/10` });
      output_sam.strengths.forEach((s: string) => {
        messages.push({ judge: "Sam", message: `✅ ${s}` });
      });
      output_sam.weakness.forEach((w: string) => {
        messages.push({ judge: "Sam", message: `⚠️ ${w}` });
      });
    }

    if (output_jordan) {
      messages.push({ judge: "Jordan", message: `Impact Score: ${output_jordan.score}/10` });
      messages.push({ judge: "Jordan", message: `🌍 ${output_jordan.impact}` });
      output_jordan.evidence_of_real_world_value.forEach((e: string) => {
        messages.push({ judge: "Jordan", message: e });
      });
    }
  }

  return messages;
};

export default function Home() {
  const [messages, setMessages] = useState<any[]>([]);
  const [status, setStatus] = useState<'idle' | 'loading' | 'streaming'>('idle');

  const startRoast = (url: string) => {
    setStatus('loading');
    
    // Switch between DEMO mode and REAL API mode
    const isDemo = false; // CHANGE THIS TO 'false' WHEN DAVIN GIVES YOU THE URL

    if (isDemo) {
      setTimeout(() => setStatus('streaming'), 2000);
      MOCK_STREAM.forEach((item, index) => {
        setTimeout(() => {
          setMessages((prev) => [...prev, item]);
        }, 2000 + (index * 1500));
      });
    } else {
      // REAL API CALL
      const eventSource = new EventSource(`http://localhost:8000/analyze/?url=${encodeURIComponent(url)}`);
      setStatus('streaming');
      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        const transformed = transformBackendData(data);
        if (transformed.length > 0) {
          setMessages((prev) => [...prev, ...transformed])
        }
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