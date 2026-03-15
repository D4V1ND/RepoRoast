export default function Arena({ messages }: { messages: any[] }) {
  return (
    <div className="max-w-4xl mx-auto mt-10 p-6 bg-gray-900 rounded-xl border border-gray-800">
      <h3 className="text-xl font-bold mb-4 text-gray-300">Live Debate</h3>
      <div className="space-y-4 h-96 overflow-y-auto">
        {messages.map((msg, i) => (
          <div key={i} className="p-4 rounded-lg bg-gray-800 border-l-4 border-red-500">
            <span className="font-bold text-red-400">{msg.judge}: </span>
            <span className="text-gray-200">{msg.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
}