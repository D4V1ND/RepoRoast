import { useState } from 'react';

export default function InputForm({ onRoast }: { onRoast: (url: string) => void }) {
  const [url, setUrl] = useState('');

  return (
    <div className="flex flex-col items-center justify-center p-10 mt-20">
      <h2 className="text-4xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-orange-500">
        Ready to get roasted?
      </h2>
      <div className="flex w-full max-w-lg gap-2">
        <input
          type="text"
          placeholder="Paste GitHub repo URL..."
          className="flex-1 p-3 rounded-lg bg-gray-900 border border-gray-700 text-white focus:outline-none focus:border-red-500"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button 
          onClick={() => onRoast(url)}
          className="px-6 py-3 bg-red-600 hover:bg-red-700 rounded-lg font-bold text-white transition-all"
        >
          ROAST
        </button>
      </div>
    </div>
  );
}