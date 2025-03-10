import { configureStore } from '@reduxjs/toolkit';
import productReducer from './slices/productSlice';
import shipmentReducer from './slices/shipmentSlice';
import orderReducer from './slices/orderSlice';

export const store = configureStore({
  reducer: {
    product: productReducer,
    shipment: shipmentReducer,
    order: orderReducer
  }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 