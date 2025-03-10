import React from 'react';

// 模拟批次数据
const mockBatches = [
    {
        id: 'BT20240118001',
        productName: 'Organic Vegetables Set',
        productionDate: '2024-01-18',
        quantity: 1000,
        status: 'producing',
        rfidCount: 850,
        qcStatus: 'pending'
    },
    {
        id: 'BT20240117002',
        productName: 'Fresh Fruit Package',
        productionDate: '2024-01-17',
        quantity: 500,
        status: 'completed',
        rfidCount: 500,
        qcStatus: 'passed'
    }
];

const Batch: React.FC = () => {
    return (
        <div className="container mt-4">
            <h2>
                Batch Management
                <small className="d-block text-muted">批次管理</small>
            </h2>

            {/* 操作按钮 */}
            <div className="mb-4">
                <button className="btn btn-primary me-2">
                    New Batch
                    <small className="d-block">新建批次</small>
                </button>
                <button className="btn btn-success">
                    Import Data
                    <small className="d-block">导入数据</small>
                </button>
            </div>

            {/* 批次列表 */}
            <div className="card">
                <div className="card-body">
                    <div className="table-responsive">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Batch ID 批次号</th>
                                    <th>Product 商品</th>
                                    <th>Date 日期</th>
                                    <th>Quantity 数量</th>
                                    <th>RFID Status RFID状态</th>
                                    <th>QC Status 质检状态</th>
                                    <th>Actions 操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                {mockBatches.map(batch => (
                                    <tr key={batch.id}>
                                        <td>{batch.id}</td>
                                        <td>{batch.productName}</td>
                                        <td>{batch.productionDate}</td>
                                        <td>{batch.quantity}</td>
                                        <td>
                                            <div className="progress" style={{ height: '20px' }}>
                                                <div 
                                                    className="progress-bar" 
                                                    role="progressbar"
                                                    style={{ width: `${(batch.rfidCount/batch.quantity)*100}%` }}
                                                >
                                                    {batch.rfidCount}/{batch.quantity}
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <span className={`badge bg-${batch.qcStatus === 'passed' ? 'success' : 'warning'}`}>
                                                {batch.qcStatus === 'passed' ? 'Passed 已通过' : 'Pending 待检'}
                                            </span>
                                        </td>
                                        <td>
                                            <button className="btn btn-sm btn-info me-2">
                                                Details
                                                <small className="d-block">详情</small>
                                            </button>
                                            <button className="btn btn-sm btn-warning me-2">
                                                RFID
                                                <small className="d-block">标签</small>
                                            </button>
                                            <button className="btn btn-sm btn-success">
                                                QC
                                                <small className="d-block">质检</small>
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            {/* 新建批次模态框 */}
            <div className="modal fade" id="newBatchModal">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title">
                                New Batch
                                <small className="d-block text-muted">新建批次</small>
                            </h5>
                            <button type="button" className="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div className="modal-body">
                            <form>
                                <div className="mb-3">
                                    <label className="form-label">
                                        Product
                                        <small className="d-block text-muted">商品</small>
                                    </label>
                                    <select className="form-select">
                                        <option>Select Product 选择商品</option>
                                    </select>
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">
                                        Quantity
                                        <small className="d-block text-muted">数量</small>
                                    </label>
                                    <input type="number" className="form-control" />
                                </div>
                            </form>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-primary">
                                Create
                                <small className="d-block">创建</small>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Batch; 