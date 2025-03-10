import React, { useState } from 'react';
import { Table, Button, Modal, Form, InputNumber, message } from 'antd';
import type { ColumnsType } from 'antd/es/table';

interface Product {
    id: string;
    name: string;
    description: string;
    price: number;
    status: string;
    stock: number;
}

const RetailerProducts: React.FC = () => {
    const [products, setProducts] = useState<Product[]>([
        {
            id: 'PROD001',
            name: 'Fresh Fruits Package',
            description: 'Assorted fresh fruits selection',
            price: 39.9,
            status: 'In Stock',
            stock: 50
        },
        {
            id: 'PROD002',
            name: 'Organic Vegetables Set',
            description: 'Fresh organic vegetables from local farm',
            price: 45.5,
            status: 'In Stock',
            stock: 30
        }
    ]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
    const [form] = Form.useForm();

    const columns: ColumnsType<Product> = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'Description',
            dataIndex: 'description',
            key: 'description',
        },
        {
            title: 'Price',
            dataIndex: 'price',
            key: 'price',
            render: (price: number) => `£${price}`
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
        },
        {
            title: 'Stock',
            dataIndex: 'stock',
            key: 'stock',
        },
        {
            title: 'Actions',
            key: 'actions',
            render: (_, record) => (
                <Button 
                    type="primary"
                    onClick={() => handleEditPrice(record)}
                >
                    Update Price
                </Button>
            ),
        }
    ];

    const handleEditPrice = (product: Product) => {
        setSelectedProduct(product);
        form.setFieldsValue({ price: product.price });
        setIsModalVisible(true);
    };

    const handleUpdatePrice = async (values: { price: number }) => {
        if (selectedProduct) {
            try {
                // 这里应该调用API更新价格
                setProducts(products.map(p => 
                    p.id === selectedProduct.id ? { ...p, price: values.price } : p
                ));
                message.success('Price updated successfully');
                setIsModalVisible(false);
            } catch (error) {
                message.error('Failed to update price');
            }
        }
    };

    return (
        <div className="container mt-4">
            <h2>Product Management</h2>
            <Table columns={columns} dataSource={products} rowKey="id" />

            <Modal
                title="Update Price"
                visible={isModalVisible}
                onCancel={() => setIsModalVisible(false)}
                footer={null}
            >
                <Form
                    form={form}
                    onFinish={handleUpdatePrice}
                    layout="vertical"
                >
                    <Form.Item
                        name="price"
                        label="New Price"
                        rules={[{ required: true, message: 'Please input new price' }]}
                    >
                        <InputNumber
                            min={0}
                            precision={2}
                            prefix="£"
                            style={{ width: '100%' }}
                        />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Update
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default RetailerProducts; 