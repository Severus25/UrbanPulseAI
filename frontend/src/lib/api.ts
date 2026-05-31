const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8100";

export async function fetchTrafficData(lat: number, lon: number, radiusKm: number = 5) {
  const res = await fetch(
    `${API_URL}/api/v1/traffic/current?lat=${lat}&lon=${lon}&radius_km=${radiusKm}`
  );
  return res.json();
}

export async function fetchTrafficForecast(lat: number, lon: number, hours: number = 2) {
  const res = await fetch(
    `${API_URL}/api/v1/traffic/forecast?lat=${lat}&lon=${lon}&horizon_hours=${hours}`
  );
  return res.json();
}

export async function fetchWeather(lat: number, lon: number) {
  const res = await fetch(`${API_URL}/api/v1/weather/current?lat=${lat}&lon=${lon}`);
  return res.json();
}

export async function fetchIncidents(lat: number, lon: number, radiusKm: number = 10) {
  const res = await fetch(
    `${API_URL}/api/v1/incidents/active?lat=${lat}&lon=${lon}&radius_km=${radiusKm}`
  );
  return res.json();
}

export async function fetchRiskScore(segmentId: string) {
  const res = await fetch(`${API_URL}/api/v1/incidents/risk?segment_id=${segmentId}`);
  return res.json();
}

export async function queryAI(query: string, location?: { lat: number; lon: number }) {
  const res = await fetch(`${API_URL}/api/v1/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, location }),
  });
  return res.json();
}
