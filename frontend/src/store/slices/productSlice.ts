import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ProductState {
  products: any[];
  loading: boolean;
  error: string | null;
}

const initialState: ProductState = {
  products: [],
  loading: false,
  error: null
};

const productSlice = createSlice({
  name: 'product',
  initialState,
  reducers: {
    setProducts: (state, action: PayloadAction<any[]>) => {
      state.products = action.payload;
    }
  }
});

export const { setProducts } = productSlice.actions;
export default productSlice.reducer; 