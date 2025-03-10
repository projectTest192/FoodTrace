import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Button, Modal, InputNumber, message, Select, DatePicker } from 'antd';
import { ShoppingCartOutlined, HistoryOutlined } from '@ant-design/icons';
import moment from 'moment';
import '../../styles/layout.css';

const { Meta } = Card;
const { RangePicker } = DatePicker;

// 静态数据
const mockProducts = [
    {
        id: 'PROD001',
        name: 'Fresh Fruits Package',
        description: 'Assorted fresh fruits selection',
        producer: 'OBU Food Science Lab',
        productDate: '2024-03-15',
        price: 39.9,
        status: 'active',
        image: '/images/freshFruitsPackage.jpg',
        rfidId: 'RF001',
        temperature: 4.5,
        humidity: 45.2,
        latitude: 51.755234,
        longitude: -1.224377
    },
    {
        id: 'PROD002',
        name: 'Organic Vegetables Set',
        description: 'Fresh organic vegetables from local farm',
        producer: 'OBU Food Science Lab',
        productDate: '2024-03-16',
        price: 45.5,
        status: 'active',
        image: '/images/OrganicVegetablesSet.jpg',
        rfidId: 'RF002',
        temperature: 4.8,
        humidity: 46.1,
        latitude: 51.754847,
        longitude: -1.223824
    }
];

const mockProducers = [
    'Green Farm Co., Ltd. / 绿色农场有限公司',
    'Fresh Foods Inc. / 鲜食品公司'
];

const ConsumerProducts: React.FC = () => {
    const [products, setProducts] = useState(mockProducts);
    const [selectedProduct, setSelectedProduct] = useState<any>(null);
    const [quantity, setQuantity] = useState(1);
    const [orderVisible, setOrderVisible] = useState(false);
    const [producers] = useState(mockProducers);

    const handleProducerFilter = (producer: string) => {
        if (!producer) {
            setProducts(mockProducts);
        } else {
            setProducts(mockProducts.filter(p => p.producer === producer));
        }
    };

    const handleBuy = (product: any) => {
        setSelectedProduct(product);
        setOrderVisible(true);
    };

    const handleOrder = async () => {
        if (!selectedProduct) return;
        message.success('Order placed successfully / 下单成功');
        setOrderVisible(false);
    };

    const handleTrace = (id: string) => {
        // Implementation of handleTrace function
        console.log(`Trace product with ID: ${id}`);
    };

    return (
        <div className="container mt-4">
            <div className="row mb-4">
                <div className="col">
                    <h2>Products List</h2>
                    
                    {/* 只保留生产商筛选 */}
                    <div className="mb-4">
                        <Select
                            style={{ width: 300 }}
                            placeholder="Select Producer"
                            onChange={handleProducerFilter}
                            allowClear
                        >
                            {producers.map(p => (
                                <Select.Option key={p} value={p}>{p}</Select.Option>
                            ))}
                        </Select>
                    </div>
                </div>
            </div>

            {/* 商品列表 */}
            <Row gutter={[16, 16]}>
                {products.map(product => (
                    <Col key={product.id} xs={24} sm={12} md={8} lg={6}>
                        <Card
                            hoverable
                            cover={
                                <img
                                    alt={product.name}
                                    src={product.image}
                                    style={{ height: 200, objectFit: 'cover' }}
                                    onError={(e) => {
                                        const img = e.target as HTMLImageElement;
                                        img.src = '/images/placeholder.jpg';
                                        img.onerror = null;
                                    }}
                                />
                            }
                        >
                            <Meta
                                title={product.name}
                                description={product.description}
                            />
                            <div className="mt-2">
                                <p>Price: £{product.price}</p>
                                <div className="button-group">
                                    <Button 
                                        type="primary" 
                                        icon={<ShoppingCartOutlined />}
                                        onClick={() => handleBuy(product)}
                                        style={{ marginRight: 8 }}
                                    >
                                        Purchase
                                    </Button>
                                    <Button
                                        icon={<HistoryOutlined />}
                                        onClick={() => handleTrace(product.id)}
                                    >
                                        Trace
                                    </Button>
                                </div>
                            </div>
                        </Card>
                    </Col>
                ))}
            </Row>

            {/* 下单弹窗 */}
            <Modal
                title="Confirm Order / 确认订单"
                visible={orderVisible}
                onOk={handleOrder}
                onCancel={() => setOrderVisible(false)}
            >
                {selectedProduct && (
                    <div>
                        <p>Product / 商品: {selectedProduct.name}</p>
                        <p>Unit Price / 单价: ¥{selectedProduct.price}</p>
                        <p>
                            Quantity / 数量: 
                            <InputNumber
                                min={1}
                                value={quantity}
                                onChange={value => setQuantity(value || 1)}
                            />
                        </p>
                        <p>Total Amount / 总价: ¥{selectedProduct.price * quantity}</p>
                    </div>
                )}
            </Modal>
        </div>
    );
};

export default ConsumerProducts; 