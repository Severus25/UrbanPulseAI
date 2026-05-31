import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "UrbanPulse AI - City Digital Twin",
  description:
    "Real-time AI platform for traffic, transit, weather, and risk-aware mobility",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased bg-gray-950 text-white">{children}</body>
    </html>
  );
}
