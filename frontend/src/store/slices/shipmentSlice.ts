import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ShipmentState {
  shipments: any[];
  loading: boolean;
  error: string | null;
}

const initialState: ShipmentState = {
  shipments: [],
  loading: false,
  error: null
};

const shipmentSlice = createSlice({
  name: 'shipment',
  initialState,
  reducers: {
    setShipments: (state, action: PayloadAction<any[]>) => {
      state.shipments = action.payload;
    }
  }
});

export const { setShipments } = shipmentSlice.actions;
export default shipmentSlice.reducer;