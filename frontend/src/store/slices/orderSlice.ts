import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface OrderState {
  orders: any[];
  loading: boolean;
  error: string | null;
}

const initialState: OrderState = {
  orders: [],
  loading: false,
  error: null
};

const orderSlice = createSlice({
  name: 'order',
  initialState,
  reducers: {
    setOrders: (state, action: PayloadAction<any[]>) => {
      state.orders = action.payload;
    }
  }
});

export const { setOrders } = orderSlice.actions;
export default orderSlice.reducer; 