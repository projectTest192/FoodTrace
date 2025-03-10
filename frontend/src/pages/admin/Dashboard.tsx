import React from 'react';
import { Card, Row, Col, Table } from 'antd';

const AdminDashboard: React.FC = () => {
    // 系统日志数据
    const logData = [
        {
            time: '2024-01-18 10:30:15',
            event: 'System configuration updated'
        },
        {
            time: '2024-01-18 10:28:30',
            event: 'New user registered: user123'
        }
    ];

    // 日志表格列定义
    const logColumns = [
        {
            title: 'Time',
            dataIndex: 'time',
            key: 'time',
        },
        {
            title: 'Event',
            dataIndex: 'event',
            key: 'event',
        }
    ];

    return (
        <div className="container mt-4">
            <h2>Admin Dashboard</h2>
            
            {/* Statistics Cards */}
            <Row gutter={[16, 16]} className="mb-4">
                <Col xs={24} sm={12} md={6}>
                    <Card className="text-white bg-primary">
                        <h5>Total Users</h5>
                        <h2>1,234</h2>
                    </Card>
                </Col>
                <Col xs={24} sm={12} md={6}>
                    <Card className="text-white bg-success">
                        <h5>Total Products</h5>
                        <h2>567</h2>
                    </Card>
                </Col>
                <Col xs={24} sm={12} md={6}>
                    <Card className="text-white bg-info">
                        <h5>Today's Orders</h5>
                        <h2>89</h2>
                    </Card>
                </Col>
                <Col xs={24} sm={12} md={6}>
                    <Card className="text-white bg-warning">
                        <h5>Pending Tasks</h5>
                        <h2>12</h2>
                    </Card>
                </Col>
            </Row>

            {/* System Configuration */}
            <Card title="System Configuration" className="mb-4">
                <Row gutter={[16, 16]}>
                    <Col span={8}>
                        <div>
                            <h6>System Name</h6>
                            <p>Food Trace System</p>
                        </div>
                    </Col>
                    <Col span={8}>
                        <div>
                            <h6>MQTT Server</h6>
                            <p>mqtt://localhost:1883</p>
                        </div>
                    </Col>
                    <Col span={8}>
                        <div>
                            <h6>Blockchain Node</h6>
                            <p>http://localhost:8545</p>
                        </div>
                    </Col>
                </Row>
            </Card>

            {/* System Logs */}
            <Card title="System Logs">
                <Table 
                    columns={logColumns}
                    dataSource={logData}
                    pagination={false}
                />
            </Card>
        </div>
    );
};

export default AdminDashboard; 