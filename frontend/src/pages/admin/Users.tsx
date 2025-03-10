import React, { useState } from 'react';
import { Table, Tag, Button, Modal, Form, Input, Select, message } from 'antd';

interface User {
    id: string;
    username: string;
    email: string;
    role: string;
    status: string;
    registerDate: string;
}

const UserManagement: React.FC = () => {
    const [users] = useState<User[]>([
        {
            id: '1',
            username: 'John Smith',
            email: 'john@example.com',
            role: 'producer',
            status: 'active',
            registerDate: '2024-01-15'
        },
        {
            id: '2',
            username: 'Mary Johnson',
            email: 'mary@example.com',
            role: 'retailer',
            status: 'active',
            registerDate: '2024-01-16'
        },
        {
            id: '3',
            username: 'David Wilson',
            email: 'david@example.com',
            role: 'consumer',
            status: 'pending',
            registerDate: '2024-01-17'
        },
        {
            id: '4',
            username: 'Sarah Brown',
            email: 'sarah@example.com',
            role: 'distributor',
            status: 'active',
            registerDate: '2024-01-18'
        }
    ]);

    const columns = [
        {
            title: 'Username',
            dataIndex: 'username',
            key: 'username',
        },
        {
            title: 'Email',
            dataIndex: 'email',
            key: 'email',
        },
        {
            title: 'Role',
            dataIndex: 'role',
            key: 'role',
            render: (role: string) => (
                <Tag color={
                    role === 'admin' ? 'red' :
                    role === 'producer' ? 'green' :
                    role === 'retailer' ? 'blue' :
                    'default'
                }>
                    {role.toUpperCase()}
                </Tag>
            )
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
            render: (status: string) => (
                <Tag color={status === 'active' ? 'green' : 'orange'}>
                    {status.toUpperCase()}
                </Tag>
            )
        },
        {
            title: 'Register Date',
            dataIndex: 'registerDate',
            key: 'registerDate',
        },
        {
            title: 'Actions',
            key: 'actions',
            render: (_: any, record: User) => (
                <span>
                    <Button type="link" onClick={() => handleEdit(record)}>
                        Edit
                    </Button>
                    <Button 
                        type="link" 
                        danger 
                        onClick={() => handleStatusChange(record)}
                    >
                        {record.status === 'active' ? 'Disable' : 'Enable'}
                    </Button>
                </span>
            ),
        }
    ];

    const handleEdit = (user: User) => {
        // 实现编辑用户功能
        message.info('Edit user: ' + user.username);
    };

    const handleStatusChange = (user: User) => {
        // 实现改变用户状态功能
        message.success(`User ${user.username} status updated`);
    };

    return (
        <div className="container mt-4">
            <h2>User Management</h2>
            <Table columns={columns} dataSource={users} rowKey="id" />
        </div>
    );
};

export default UserManagement; 