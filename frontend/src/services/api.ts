import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8002/api', // 你的后端API地址
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求拦截器
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token && config.headers) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // 未授权，清除token并跳转到登录页
                    localStorage.clear();
                    window.location.href = '/auth';
                    break;
                case 403:
                    // 权限不足
                    window.location.href = '/unauthorized';
                    break;
                default:
                    break;
            }
        }
        return Promise.reject(error);
    }
);

// 生产商API
export const producerAPI = {
    // 获取商品列表
    getProducts: () => api.get('/producer/products'),
    
    // 创建新商品
    createProduct: (data: any) => api.post('/producer/products', data),
    
    // 更新商品
    updateProduct: (id: number, data: any) => api.put(`/producer/products/${id}`, data),
    
    // 删除商品
    deleteProduct: (id: number) => api.delete(`/producer/products/${id}`),
    
    // 绑定RFID
    bindRFID: (productId: number, rfidData: any) => api.post(`/producer/products/${productId}/rfid`, rfidData)
};

// 配送商API
export const distributorAPI = {
    // 获取配送单列表
    getShipments: () => api.get('/distributor/shipments'),
    
    // 创建配送单
    createShipment: (data: any) => api.post('/distributor/shipments', data),
    
    // 更新配送单状态
    updateShipmentStatus: (id: number, status: string) => api.put(`/distributor/shipments/${id}/status`, { status })
};

// 零售商API
export const retailerAPI = {
    // 获取商品列表
    getProducts: () => api.get('/retailer/products'),
    
    // 更新商品价格
    updatePrice: (id: number, price: number) => api.put(`/retailer/products/${id}/price`, { price }),
    
    // 确认收货
    confirmReceipt: (shipmentId: number) => api.post(`/retailer/shipments/${shipmentId}/confirm`)
};

export default api; 