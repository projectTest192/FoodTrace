import React, { useState } from 'react';
import { Table, Button, Modal, Form, Input, InputNumber, Upload, message, Select } from 'antd';
import { PlusOutlined, UploadOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';

interface Product {
    id: string;
    name: string;
    description: string;
    price: number;
    category: string;
    stock: number;
    unit: string;
    shelfLife: number;
    storageConditions: string;
    image: string;
    status: string;
}

const ProductManagement: React.FC = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [isRfidModalVisible, setIsRfidModalVisible] = useState(false);
    const [form] = Form.useForm();

    const columns: ColumnsType<Product> = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'Category',
            dataIndex: 'category',
            key: 'category',
        },
        {
            title: 'Price',
            dataIndex: 'price',
            key: 'price',
            render: (price: number) => `£${price}`,
        },
        {
            title: 'Stock',
            dataIndex: 'stock',
            key: 'stock',
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
        },
        {
            title: 'Actions',
            key: 'actions',
            render: (_, record) => (
                <Button type="link" onClick={() => handleEdit(record)}>
                    Edit
                </Button>
            ),
        }
    ];

    const handleCreate = async (values: any) => {
        // 模拟创建商品
        const newProduct = {
            id: `P${Date.now()}`,
            ...values,
            status: 'pending_rfid'
        };
        setProducts([...products, newProduct]);
        setIsModalVisible(false);
        setIsRfidModalVisible(true);

        // 模拟RFID录入过程
        setTimeout(() => {
            setIsRfidModalVisible(false);
            message.success('Product created and RFID bound successfully');
        }, 5000);
    };

    const handleEdit = (product: Product) => {
        form.setFieldsValue(product);
        setIsModalVisible(true);
    };

    return (
        <div className="container mt-4">
            <div className="header-actions mb-4">
                <h2>Product Management</h2>
                <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalVisible(true)}>
                    Create Product
                </Button>
            </div>

            <Table columns={columns} dataSource={products} rowKey="id" />

            <Modal
                title="Create Product"
                visible={isModalVisible}
                onCancel={() => setIsModalVisible(false)}
                footer={null}
            >
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleCreate}
                >
                    <Form.Item name="name" label="Product Name" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="description" label="Description" rules={[{ required: true }]}>
                        <Input.TextArea />
                    </Form.Item>
                    <Form.Item name="category" label="Category" rules={[{ required: true }]}>
                        <Select>
                            <Select.Option value="fruits">Fruits</Select.Option>
                            <Select.Option value="vegetables">Vegetables</Select.Option>
                        </Select>
                    </Form.Item>
                    <Form.Item name="price" label="Price" rules={[{ required: true }]}>
                        <InputNumber prefix="£" style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item name="stock" label="Stock" rules={[{ required: true }]}>
                        <InputNumber style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item name="unit" label="Unit" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="shelfLife" label="Shelf Life (days)" rules={[{ required: true }]}>
                        <InputNumber style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item name="storageConditions" label="Storage Conditions" rules={[{ required: true }]}>
                        <Input.TextArea />
                    </Form.Item>
                    <Form.Item name="image" label="Product Image">
                        <Upload>
                            <Button icon={<UploadOutlined />}>Upload Image</Button>
                        </Upload>
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Create
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>

            <Modal
                title="RFID Binding"
                visible={isRfidModalVisible}
                footer={null}
                closable={false}
            >
                <div className="text-center">
                    <p>Waiting for RFID input...</p>
                    <div className="loading-spinner"></div>
                </div>
            </Modal>
        </div>
    );
};

export default ProductManagement; 