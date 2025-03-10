import React, { useState } from 'react';
import { Input, Button, Table, Card, Timeline, Descriptions } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';

interface BlockchainRecord {
    txId: string;
    value: {
        id: string;
        name: string;
        description: string;
        producer: string;
        productDate: string;
        status: string;
        deviceId: string;
        rfidId: string;
        temperature: number;
        humidity: number;
        latitude: number;
        longitude: number;
        writeTime: string;
    };
    timestamp: string;
    isDelete: boolean;
}

const RFIDQuery: React.FC = () => {
    const [rfidId, setRfidId] = useState('');
    const [blockchainData, setBlockchainData] = useState<BlockchainRecord[]>([]);
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        setLoading(true);
        try {
            // 模拟API调用
            const mockData: BlockchainRecord[] = [
                {
                    "txId": "12292e0b1039661cad24811ff9ea644bd718eb3b8d49a22d2c299005121afbf8",
                    "value": {
                        "id": "PROD001",
                        "name": "foodA",
                        "description": "Fresh food A",
                        "producer": "producerA",
                        "productDate": "2024-03-15",
                        "status": "sold",
                        "deviceId": "DEV001",
                        "rfidId": "RF001",
                        "temperature": 4.5,
                        "humidity": 45.2,
                        "latitude": 31.2304,
                        "longitude": 121.4737,
                        "writeTime": "2025-02-08T13:55:55.515977643Z"
                    },
                    "timestamp": "2025-02-08T13:56:07.77744Z",
                    "isDelete": false
                },
                {
                    "txId": "b7bcc15209c153c0d682ba567a1d88a8a4288f181518388d51c3718e879ee437",
                    "value": {
                        "id": "PROD001",
                        "name": "foodA",
                        "description": "Fresh food A",
                        "producer": "producerA",
                        "productDate": "2024-03-15",
                        "status": "active",
                        "deviceId": "DEV001",
                        "rfidId": "RF001",
                        "temperature": 4.5,
                        "humidity": 45.2,
                        "latitude": 31.2304,
                        "longitude": 121.4737,
                        "writeTime": "2025-02-08T13:55:55.515977643Z"
                    },
                    "timestamp": "2025-02-08T13:55:55.51343Z",
                    "isDelete": false
                }
            ];
            setBlockchainData(mockData);
        } catch (error) {
            console.error('Error fetching blockchain data:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-4">
            {/* 搜索框样式调整 */}
            <div style={{ 
                display: 'flex', 
                justifyContent: 'flex-end', 
                marginBottom: 20,
                background: '#f5f5f5',
                padding: '20px',
                borderRadius: '8px'
            }}>
                <Input.Search
                    placeholder="Enter RFID ID to search"
                    enterButton={
                        <Button type="primary" icon={<SearchOutlined />} size="large">
                            Search
                        </Button>
                    }
                    size="large"
                    style={{ width: 400 }}
                    value={rfidId}
                    onChange={(e) => setRfidId(e.target.value)}
                    onSearch={handleSearch}
                    loading={loading}
                />
            </div>

            {/* 区块链信息显示 */}
            {blockchainData.length > 0 && (
                <div>
                    <h2>Blockchain Tracing Information</h2>
                    <div className="product-info mb-4" style={{
                        background: '#fff',
                        padding: '20px',
                        borderRadius: '8px',
                        border: '1px solid #e8e8e8'
                    }}>
                        <h3>Product Information</h3>
                        <Descriptions bordered>
                            <Descriptions.Item label="Product ID">{blockchainData[0].value.id}</Descriptions.Item>
                            <Descriptions.Item label="Product Name">{blockchainData[0].value.name}</Descriptions.Item>
                            <Descriptions.Item label="Current Status">{blockchainData[0].value.status}</Descriptions.Item>
                        </Descriptions>
                    </div>
                    <Timeline mode="left">
                        {blockchainData.map((record, index) => (
                            <Timeline.Item key={record.txId}>
                                <Card>
                                    <Descriptions bordered column={2} size="small">
                                        <Descriptions.Item label="Transaction ID" span={2}>
                                            {record.txId}
                                        </Descriptions.Item>
                                        <Descriptions.Item label="Status">
                                            {record.value.status}
                                        </Descriptions.Item>
                                        <Descriptions.Item label="Device ID">
                                            {record.value.deviceId}
                                        </Descriptions.Item>
                                        <Descriptions.Item label="Temperature">
                                            {record.value.temperature}°C
                                        </Descriptions.Item>
                                        <Descriptions.Item label="Humidity">
                                            {record.value.humidity}%
                                        </Descriptions.Item>
                                        <Descriptions.Item label="Location">
                                            {record.value.latitude}°N, {record.value.longitude}°E
                                        </Descriptions.Item>
                                        <Descriptions.Item label="Write Time" span={2}>
                                            {new Date(record.value.writeTime).toLocaleString()}
                                        </Descriptions.Item>
                                    </Descriptions>
                                </Card>
                            </Timeline.Item>
                        ))}
                    </Timeline>
                </div>
            )}
        </div>
    );
};

export default RFIDQuery; 