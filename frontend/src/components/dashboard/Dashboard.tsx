"use client";

import { useState } from "react";

export function Dashboard() {
  const [activeTab, setActiveTab] = useState<"overview" | "traffic" | "risk" | "simulation">(
    "overview"
  );

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "traffic", label: "Traffic" },
    { id: "risk", label: "Risk" },
    { id: "simulation", label: "What-If" },
  ] as const;

  return (
    <div className="p-4 space-y-4">
      {/* Tab navigation */}
      <div className="flex gap-1 bg-gray-900 rounded-lg p-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
              activeTab === tab.id
                ? "bg-blue-600 text-white"
                : "text-gray-400 hover:text-white"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === "overview" && <OverviewPanel />}
      {activeTab === "traffic" && <TrafficPanel />}
      {activeTab === "risk" && <RiskPanel />}
      {activeTab === "simulation" && <SimulationPanel />}
    </div>
  );
}

function OverviewPanel() {
  return (
    <div className="space-y-3">
      <MetricCard label="Active Incidents" value="3" trend="up" />
      <MetricCard label="Avg Congestion" value="Medium" trend="stable" />
      <MetricCard label="Disruption Risk" value="0.42" trend="down" />
      <MetricCard label="Active Alerts" value="2" trend="stable" />
    </div>
  );
}

function TrafficPanel() {
  return (
    <div className="text-sm text-gray-400">
      <p>Traffic forecasts and heatmap controls will appear here.</p>
      {/* TODO: Forecast timeline, segment details, congestion chart */}
    </div>
  );
}

function RiskPanel() {
  return (
    <div className="text-sm text-gray-400">
      <p>Risk scoring and alerts will appear here.</p>
      {/* TODO: Risk heatmap toggle, segment risk details */}
    </div>
  );
}

function SimulationPanel() {
  return (
    <div className="text-sm text-gray-400">
      <p>What-if simulation controls will appear here.</p>
      {/* TODO: Scenario builder, parameter sliders, run simulation button */}
    </div>
  );
}

function MetricCard({
  label,
  value,
  trend,
}: {
  label: string;
  value: string;
  trend: "up" | "down" | "stable";
}) {
  const trendIcon = trend === "up" ? "↑" : trend === "down" ? "↓" : "→";
  const trendColor =
    trend === "up" ? "text-red-400" : trend === "down" ? "text-green-400" : "text-gray-400";

  return (
    <div className="bg-gray-900 rounded-lg p-3 flex justify-between items-center">
      <span className="text-sm text-gray-300">{label}</span>
      <div className="flex items-center gap-2">
        <span className="text-sm font-semibold">{value}</span>
        <span className={`text-xs ${trendColor}`}>{trendIcon}</span>
      </div>
    </div>
  );
}
