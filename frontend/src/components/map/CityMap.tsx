"use client";

import { useRef, useCallback } from "react";
import Map, { NavigationControl, ScaleControl } from "react-map-gl";
import { useMapStore } from "@/stores/mapStore";

const MAPBOX_TOKEN = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || "";

export function CityMap() {
  const mapRef = useRef(null);
  const { viewport, setViewport, layers } = useMapStore();

  const onMove = useCallback(
    (evt: any) => {
      setViewport(evt.viewState);
    },
    [setViewport]
  );

  return (
    <Map
      ref={mapRef}
      {...viewport}
      onMove={onMove}
      mapboxAccessToken={MAPBOX_TOKEN}
      mapStyle="mapbox://styles/mapbox/dark-v11"
      style={{ width: "100%", height: "100%" }}
    >
      <NavigationControl position="top-left" />
      <ScaleControl position="bottom-left" />

      {/* TODO: Add Deck.gl overlay layers */}
      {/* - Traffic heatmap layer */}
      {/* - Incident markers layer */}
      {/* - Risk overlay layer */}
      {/* - Route recommendation layer */}
    </Map>
  );
}
