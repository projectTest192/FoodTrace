import React, { useState } from 'react';
import { Table, Tag, Card, Row, Col, Typography } from 'antd';
import type { ColumnsType } from 'antd/es/table';

const { Title, Text } = Typography;

// 统一的订单状态枚举
export enum OrderStatus {
    PENDING = 'pending',
    COMPLETED = 'completed',
    CANCELLED = 'cancelled'
}

// 统一的状态显示文本
const statusTextMap = {
    [OrderStatus.PENDING]: 'Pending Payment',
    [OrderStatus.COMPLETED]: 'Completed',
    [OrderStatus.CANCELLED]: 'Cancelled'
};

// 统一的状态标签颜色
const statusColorMap = {
    [OrderStatus.PENDING]: 'processing',
    [OrderStatus.COMPLETED]: 'success',
    [OrderStatus.CANCELLED]: 'error'
};

interface OrderItem {
    id: string;
    productName: string;
    quantity: number;
    price: number;
    subtotal: number;
}

interface Order {
    id: string;
    orderDate: string;
    status: OrderStatus;
    items: OrderItem[];
    total: number;
}

const Orders: React.FC = () => {
    // 示例订单数据
    const [orders] = useState<Order[]>([
        {
            id: 'ORD20240101001',
            orderDate: '2024-01-01',
            status: OrderStatus.COMPLETED,
            items: [
                {
                    id: 'ITEM001',
                    productName: 'Organic Vegetables Set',
                    quantity: 1,
                    price: 39.90,
                    subtotal: 39.90
                },
                {
                    id: 'ITEM002',
                    productName: 'Fresh Fruit Package',
                    quantity: 1,
                    price: 45.50,
                    subtotal: 45.50
                }
            ],
            total: 85.40
        },
        {
            id: 'ORD20240102002',
            orderDate: '2024-01-02',
            status: OrderStatus.PENDING,
            items: [
                {
                    id: 'ITEM003',
                    productName: 'Organic Vegetables Set',
                    quantity: 1,
                    price: 39.90,
                    subtotal: 39.90
                }
            ],
            total: 39.90
        }
    ]);

    const itemColumns: ColumnsType<OrderItem> = [
        {
            title: 'Product',
            dataIndex: 'productName',
            key: 'productName',
        },
        {
            title: 'Quantity',
            dataIndex: 'quantity',
            key: 'quantity',
        },
        {
            title: 'Price',
            dataIndex: 'price',
            key: 'price',
            render: (price: number) => `¥${price.toFixed(2)}`,
        },
        {
            title: 'Subtotal',
            dataIndex: 'subtotal',
            key: 'subtotal',
            render: (subtotal: number) => `¥${subtotal.toFixed(2)}`,
        },
    ];

    return (
        <div className="orders-page">
            <Title level={2}>My Orders</Title>
            {orders.map(order => (
                <Card 
                    key={order.id} 
                    className="order-card"
                    style={{ marginBottom: 16 }}
                >
                    <Row justify="space-between" align="middle" style={{ marginBottom: 16 }}>
                        <Col>
                            <Text strong>Order ID: {order.id}</Text>
                            <br />
                            <Text>Order Date: {order.orderDate}</Text>
                        </Col>
                        <Col>
                            <Tag color={statusColorMap[order.status]}>
                                {statusTextMap[order.status]}
                            </Tag>
                        </Col>
                    </Row>

                    <Table
                        columns={itemColumns}
                        dataSource={order.items}
                        pagination={false}
                        rowKey="id"
                        summary={() => (
                            <Table.Summary>
                                <Table.Summary.Row>
                                    <Table.Summary.Cell index={0} colSpan={3}>
                                        <Text strong>Total:</Text>
                                    </Table.Summary.Cell>
                                    <Table.Summary.Cell index={1}>
                                        <Text strong>¥{order.total.toFixed(2)}</Text>
                                    </Table.Summary.Cell>
                                </Table.Summary.Row>
                            </Table.Summary>
                        )}
                    />
                </Card>
            ))}
        </div>
    );
};

export default Orders; 