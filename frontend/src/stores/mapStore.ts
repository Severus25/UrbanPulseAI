import { create } from "zustand";

interface ViewportState {
  longitude: number;
  latitude: number;
  zoom: number;
  pitch: number;
  bearing: number;
}

interface MapStore {
  viewport: ViewportState;
  setViewport: (viewport: ViewportState) => void;
  layers: {
    traffic: boolean;
    risk: boolean;
    incidents: boolean;
    transit: boolean;
  };
  toggleLayer: (layer: keyof MapStore["layers"]) => void;
}

export const useMapStore = create<MapStore>((set) => ({
  viewport: {
    longitude: -73.935242, // NYC default
    latitude: 40.73061,
    zoom: 12,
    pitch: 45,
    bearing: 0,
  },
  setViewport: (viewport) => set({ viewport }),
  layers: {
    traffic: true,
    risk: false,
    incidents: true,
    transit: false,
  },
  toggleLayer: (layer) =>
    set((state) => ({
      layers: { ...state.layers, [layer]: !state.layers[layer] },
    })),
}));
