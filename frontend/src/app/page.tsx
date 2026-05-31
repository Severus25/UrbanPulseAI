"use client";

import { CityMap } from "@/components/map/CityMap";
import { Dashboard } from "@/components/dashboard/Dashboard";
import { AIPanel } from "@/components/dashboard/AIPanel";

export default function HomePage() {
  return (
    <main className="h-screen w-screen flex">
      {/* Map takes 2/3 of screen */}
      <div className="flex-1 relative">
        <CityMap />
      </div>

      {/* Right panel: Dashboard + AI */}
      <aside className="w-[420px] border-l border-gray-800 flex flex-col overflow-hidden">
        <header className="p-4 border-b border-gray-800">
          <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            🏙️ UrbanPulse AI
          </h1>
          <p className="text-xs text-gray-400 mt-1">
            City Digital Twin • Real-time Intelligence
          </p>
        </header>

        <div className="flex-1 overflow-y-auto">
          <Dashboard />
        </div>

        <div className="border-t border-gray-800">
          <AIPanel />
        </div>
      </aside>
    </main>
  );
}
