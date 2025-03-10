import React, { useState } from 'react';

// 模拟质检数据
const mockInspections = [
    {
        id: 'QC20240118001',
        productName: 'Organic Vegetables Set',
        batch: 'BT20240118001',
        date: '2024-01-18',
        status: 'pending',
        items: [
            { name: '外观检查', status: 'pending' },
            { name: '农残检测', status: 'pending' },
            { name: '包装完整性', status: 'pending' }
        ]
    }
];

const Inspection: React.FC = () => {
    const [activeTab, setActiveTab] = useState('pending');

    return (
        <div className="container mt-4">
            <h2>
                Quality Inspection
                <small className="d-block text-muted">质量检查</small>
            </h2>

            <div className="card mt-4">
                <div className="card-body">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Product 商品</th>
                                <th>Batch 批次</th>
                                <th>Date 日期</th>
                                <th>Status 状态</th>
                                <th>Actions 操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            {mockInspections.map(inspection => (
                                <tr key={inspection.id}>
                                    <td>{inspection.id}</td>
                                    <td>{inspection.productName}</td>
                                    <td>{inspection.batch}</td>
                                    <td>{inspection.date}</td>
                                    <td>
                                        <span className="badge bg-warning">
                                            Pending 待检查
                                        </span>
                                    </td>
                                    <td>
                                        <button className="btn btn-sm btn-primary">
                                            Start
                                            <small className="d-block">开始检查</small>
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Inspection; 