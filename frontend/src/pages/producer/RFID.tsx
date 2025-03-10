import React, { useState } from 'react';

// 模拟商品数据
const mockProducts = [
    { id: 1, name: 'Organic Vegetables Set', batch: 'BT20240118001' },
    { id: 2, name: 'Fresh Fruit Package', batch: 'BT20240118002' }
];

const RFID: React.FC = () => {
    const [selectedProduct, setSelectedProduct] = useState('');
    const [rfidCode, setRfidCode] = useState('');

    const handleRFIDBinding = async () => {
        // TODO: 调用后端API，将RFID与商品绑定
        // TODO: 通过MQTT将数据写入RFID标签
        // TODO: 将关键信息上传至区块链
        console.log('Binding RFID:', { product: selectedProduct, rfid: rfidCode });
    };

    return (
        <div className="container mt-4">
            <h2>
                RFID Management
                <small className="d-block text-muted">RFID管理</small>
            </h2>

            <div className="card mt-4">
                <div className="card-body">
                    <div className="row">
                        <div className="col-md-6">
                            <div className="mb-3">
                                <label className="form-label">
                                    Select Product
                                    <small className="d-block text-muted">选择商品</small>
                                </label>
                                <select 
                                    className="form-select"
                                    value={selectedProduct}
                                    onChange={(e) => setSelectedProduct(e.target.value)}
                                >
                                    <option value="">Select Product 选择商品</option>
                                    {mockProducts.map(product => (
                                        <option key={product.id} value={product.id}>
                                            {product.name} - {product.batch}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div className="mb-3">
                                <label className="form-label">
                                    RFID Code
                                    <small className="d-block text-muted">RFID编码</small>
                                </label>
                                <input 
                                    type="text" 
                                    className="form-control"
                                    value={rfidCode}
                                    onChange={(e) => setRfidCode(e.target.value)}
                                />
                            </div>
                            <button 
                                className="btn btn-primary"
                                onClick={handleRFIDBinding}
                                disabled={!selectedProduct || !rfidCode}
                            >
                                Bind RFID
                                <small className="d-block">绑定RFID</small>
                            </button>
                        </div>
                        <div className="col-md-6">
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">
                                        RFID Reader Status
                                        <small className="d-block text-muted">RFID读写器状态</small>
                                    </h5>
                                    <div className="alert alert-success">
                                        Reader Connected
                                        <small className="d-block">读写器已连接</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RFID; 