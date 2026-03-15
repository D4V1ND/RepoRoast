'use client';
import ResultsChart from "@/components/RadarChart";

export default function Arena({ messages }: { messages: any[] }) {
  
  const downloadReport = () => {
    const content = messages.map(m => `${m.judge}: ${m.message}`).join('\n');
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'roast-report.txt';
    a.click();
  };

  const shareResult = () => {
    navigator.clipboard.writeText(window.location.href);
    alert("Link copied! Share your roast with the team.");
  };

  return (
    <div className="max-w-6xl mx-auto mt-10 p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
      {/* LEFT: The Feed */}
      <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 shadow-2xl">
        <h3 className="text-xl font-bold mb-4 text-white">Live Debate</h3>
        <div className="space-y-4 h-[500px] overflow-y-auto pr-2">
          {messages.map((msg, i) => (
            <div key={i} className="p-4 rounded-lg bg-gray-800 border-l-4 border-red-500 animate-in fade-in slide-in-from-bottom-2">
              <span className="font-bold text-red-400">{msg.judge}: </span>
              <span className="text-gray-200">{msg.message}</span>
            </div>
          ))}
        </div>
      </div>

      {/* RIGHT: The Dashboard */}
      <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 flex flex-col items-center justify-center">
        <h3 className="text-xl font-bold mb-4 text-white">Analysis Score</h3>
        <ResultsChart />
        
        <div className="mt-8 flex gap-4">
          <button onClick={downloadReport} className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded text-sm border border-gray-600 transition">
            Download Report
          </button>
          <button onClick={shareResult} className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded text-sm font-bold transition">
            Share Roast
          </button>
        </div>
        
        <div className="mt-8 text-center text-gray-500 text-sm">
           <p>Agents evaluating: <span className="text-red-500 font-bold">INNOVATION, ARCHITECTURE, IMPACT</span></p>
        </div>
      </div>
    </div>
  );
}