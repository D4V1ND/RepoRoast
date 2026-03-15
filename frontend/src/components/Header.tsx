export default function Header() {
  return (
    <header className="w-full p-6 border-b border-gray-800 bg-gray-950 text-white flex justify-between items-center">
      <h1 className="text-2xl font-bold tracking-tighter text-white">
        Repo<span className="text-red-500">Roast</span>
      </h1>
      <div className="text-xs text-gray-400 font-mono">v1.0.0</div>
    </header>
  );
}