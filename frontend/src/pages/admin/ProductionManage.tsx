import React, { useState } from 'react';
import { Table, Button, Space, Tag } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import ProductCreate from './ProductCreate';

const ProductionManage: React.FC = () => {
    const [createModalVisible, setCreateModalVisible] = useState(false);
    
    // 示例数据
    const [products] = useState([
        {
            id: 'PROD001',
            name: 'Fresh Apple',
            description: 'Premium quality fresh apples from local farms',
            price: 29.90,
            stock: 1000,
            category: 'fruits',
            unit: 'kg',
            expiryDate: 15,
            storageCondition: 'refrigerated',
            image: '/images/apple.jpg'
        },
        {
            id: 'PROD002',
            name: 'Organic Vegetables Pack',
            description: 'Mixed organic vegetables selection',
            price: 45.50,
            stock: 500,
            category: 'vegetables',
            unit: 'box',
            expiryDate: 7,
            storageCondition: 'refrigerated',
            image: '/images/vegetables.jpg'
        },
        {
            id: 'PROD003',
            name: 'Premium Beef',
            description: 'High-quality beef cuts',
            price: 128.00,
            stock: 200,
            category: 'meat',
            unit: 'kg',
            expiryDate: 10,
            storageCondition: 'frozen',
            image: '/images/beef.jpg'
        }
    ]);

    const columns = [
        {
            title: 'Product ID',
            dataIndex: 'id',
            key: 'id',
        },
        {
            title: 'Product Name',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'Description',
            dataIndex: 'description',
            key: 'description',
            ellipsis: true,
        },
        {
            title: 'Price',
            dataIndex: 'price',
            key: 'price',
            render: (price: number) => `¥${price.toFixed(2)}`,
        },
        {
            title: 'Stock',
            dataIndex: 'stock',
            key: 'stock',
        },
        {
            title: 'Category',
            dataIndex: 'category',
            key: 'category',
            render: (category: string) => {
                const colorMap: { [key: string]: string } = {
                    fruits: 'green',
                    vegetables: 'cyan',
                    meat: 'red',
                    seafood: 'blue'
                };
                return <Tag color={colorMap[category]}>{category.toUpperCase()}</Tag>;
            },
        },
        {
            title: 'Storage',
            dataIndex: 'storageCondition',
            key: 'storageCondition',
            render: (condition: string) => {
                const colorMap: { [key: string]: string } = {
                    room: 'default',
                    refrigerated: 'blue',
                    frozen: 'purple'
                };
                return <Tag color={colorMap[condition]}>{condition.toUpperCase()}</Tag>;
            },
        },
        {
            title: 'Action',
            key: 'action',
            render: (text: any, record: any) => (
                <Space size="middle">
                    <Button type="link">Edit</Button>
                    <Button type="link" danger>Delete</Button>
                </Space>
            ),
        },
    ];

    const handleCreateSuccess = () => {
        setCreateModalVisible(false);
        // TODO: 刷新商品列表
    };

    return (
        <div className="production-manage">
            <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: 16 
            }}>
                <h2>Production Management</h2>
                <Button
                    type="primary"
                    icon={<PlusOutlined />}
                    onClick={() => setCreateModalVisible(true)}
                >
                    Create Product
                </Button>
            </div>

            <Table
                columns={columns}
                dataSource={products}
                rowKey="id"
                pagination={{
                    pageSize: 10,
                    showTotal: (total) => `Total ${total} items`
                }}
            />

            <ProductCreate
                visible={createModalVisible}
                onCancel={() => setCreateModalVisible(false)}
                onSuccess={handleCreateSuccess}
            />
        </div>
    );
};

export default ProductionManage; 