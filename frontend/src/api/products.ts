import api from './axios';

// Define a type for the product
export interface Product {
  id: number;
  name: string;
  price: number;
}

interface OrderData {
  productId: number;
  quantity: number;
}

export const getProducts = async (): Promise<Product[]> => {
  const response = await api.get<Product[]>('/products');
  return response.data;
};

export const placeOrder = async (orderData: OrderData): Promise<void> => {
  await api.post('/orders', orderData);
}; 