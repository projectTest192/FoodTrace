import React, { useState } from 'react';
import { Table, Tag, Space, Button } from 'antd';
import type { ColumnsType } from 'antd/es/table';

// 修改订单状态枚举
export enum OrderStatus {
    PENDING = 'pending',
    COMPLETED = 'completed',
    CANCELLED = 'cancelled'
}

// 状态显示文本映射
const statusTextMap = {
    [OrderStatus.PENDING]: 'Pending Payment',
    [OrderStatus.COMPLETED]: 'Completed',
    [OrderStatus.CANCELLED]: 'Cancelled'
};

// 状态标签颜色映射
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
}

interface Order {
    id: string;
    customerName: string;
    orderDate: string;
    status: OrderStatus;
    items: OrderItem[];
    total: number;
}

const Orders: React.FC = () => {
    // 示例订单数据
    const [orders] = useState<Order[]>([
        {
            id: 'ORD001',
            customerName: 'John Doe',
            orderDate: '2024-03-15',
            status: OrderStatus.COMPLETED,
            items: [
                {
                    id: 'ITEM001',
                    productName: 'Fresh Apple',
                    quantity: 2,
                    price: 29.90
                }
            ],
            total: 59.80
        },
        {
            id: 'ORD002',
            customerName: 'Jane Smith',
            orderDate: '2024-03-16',
            status: OrderStatus.PENDING,
            items: [
                {
                    id: 'ITEM002',
                    productName: 'Organic Vegetables Pack',
                    quantity: 1,
                    price: 45.50
                }
            ],
            total: 45.50
        },
        {
            id: 'ORD003',
            customerName: 'Mike Johnson',
            orderDate: '2024-03-14',
            status: OrderStatus.CANCELLED,
            items: [
                {
                    id: 'ITEM003',
                    productName: 'Premium Beef',
                    quantity: 1,
                    price: 128.00
                }
            ],
            total: 128.00
        }
    ]);

    const columns: ColumnsType<Order> = [
        {
            title: 'Order ID',
            dataIndex: 'id',
            key: 'id',
        },
        {
            title: 'Customer',
            dataIndex: 'customerName',
            key: 'customerName',
        },
        {
            title: 'Order Date',
            dataIndex: 'orderDate',
            key: 'orderDate',
        },
        {
            title: 'Items',
            dataIndex: 'items',
            key: 'items',
            render: (items: OrderItem[]) => (
                <>
                    {items.map(item => (
                        <div key={item.id}>
                            {item.productName} x {item.quantity}
                        </div>
                    ))}
                </>
            ),
        },
        {
            title: 'Total',
            dataIndex: 'total',
            key: 'total',
            render: (total: number) => `¥${total.toFixed(2)}`,
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
            render: (status: OrderStatus) => (
                <Tag color={statusColorMap[status]}>
                    {statusTextMap[status]}
                </Tag>
            ),
        },
        {
            title: 'Action',
            key: 'action',
            render: (_, record) => (
                <Space size="middle">
                    <Button type="link">View Details</Button>
                    {record.status === OrderStatus.PENDING && (
                        <>
                            <Button 
                                type="link" 
                                onClick={() => handleStatusChange(record.id, OrderStatus.COMPLETED)}
                            >
                                Complete
                            </Button>
                            <Button 
                                type="link" 
                                danger 
                                onClick={() => handleStatusChange(record.id, OrderStatus.CANCELLED)}
                            >
                                Cancel
                            </Button>
                        </>
                    )}
                </Space>
            ),
        },
    ];

    const handleStatusChange = (orderId: string, newStatus: OrderStatus) => {
        // TODO: 实现状态更新逻辑
        console.log(`Changing order ${orderId} status to ${newStatus}`);
    };

    return (
        <div className="orders-page">
            <h2>Order Management</h2>
            <Table 
                columns={columns} 
                dataSource={orders}
                rowKey="id"
                pagination={{
                    pageSize: 10,
                    showTotal: (total) => `Total ${total} orders`
                }}
            />
        </div>
    );
};

export default Orders; 