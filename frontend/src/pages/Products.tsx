import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Product, getProducts, placeOrder } from '../api/products';

const Products: React.FC = () => {
    const navigate = useNavigate();
    const [products, setProducts] = useState<Product[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const data = await getProducts();
                setProducts(data);
            } catch (err) {
                setError('获取产品列表失败');
                console.error(err);
            }
        };
        fetchProducts();
    }, []);

    const handleOrder = async (productId: number) => {
        try {
            await placeOrder({ productId, quantity: 1 });
            alert('下单成功！');
        } catch (err) {
            console.error('下单失败', err);
            alert('下单失败，请重试');
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/auth');
    };

    return (
        <div className="container mt-5">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h1>产品列表</h1>
                <button 
                    className="btn btn-outline-danger"
                    onClick={handleLogout}
                >
                    退出登录
                </button>
            </div>
            {error && (
                <div className="alert alert-danger">{error}</div>
            )}
            {products.length === 0 ? (
                <div className="alert alert-info">
                    暂无产品数据
                </div>
            ) : (
                <div className="row">
                    {products.map((product) => (
                        <div key={product.id} className="col-md-4 mb-4">
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">{product.name}</h5>
                                    <p className="card-text">价格: ¥{product.price}</p>
                                    <button 
                                        className="btn btn-primary"
                                        onClick={() => handleOrder(product.id)}
                                    >
                                        购买
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Products; 