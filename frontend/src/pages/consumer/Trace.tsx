import React, { useState } from 'react';
import '../../styles/layout.css';

interface TraceResult {
    productName: string;
    batch: string;
    producer: string;
    productionDate: string;
    logisticInfo: {
        date: string;
        location: string;
        status: string;
    }[];
}

const Trace: React.FC = () => {
    const [batchNumber, setBatchNumber] = useState('');
    const [traceResult, setTraceResult] = useState<TraceResult | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleTrace = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        // 模拟API请求
        setTimeout(() => {
            setTraceResult({
                productName: "Organic Vegetables Set",
                batch: batchNumber,
                producer: "Green Farm Co., Ltd.",
                productionDate: "2024-01-18",
                logisticInfo: [
                    {
                        date: "2024-01-18 09:00",
                        location: "Production Facility",
                        status: "Production Completed"
                    },
                    {
                        date: "2024-01-18 14:00",
                        location: "Quality Control",
                        status: "Quality Check Passed"
                    },
                    {
                        date: "2024-01-19 10:00",
                        location: "Distribution Center",
                        status: "Ready for Delivery"
                    }
                ]
            });
            setIsLoading(false);
        }, 1000);
    };

    return (
        <div className="container">
            <h2 className="mb-4">Trace Query溯源查询</h2>
            
            <div className="card mb-4">
                <div className="card-body">
                    <form onSubmit={handleTrace}>
                        <div className="row g-3 align-items-center">
                            <div className="col-auto">
                                <label className="form-label">Batch Number批次号:</label>
                            </div>
                            <div className="col-md-4">
                                <input
                                    type="text"
                                    className="form-control"
                                    value={batchNumber}
                                    onChange={(e) => setBatchNumber(e.target.value)}
                                    placeholder="Enter batch number输入批次号"
                                    required
                                />
                            </div>
                            <div className="col-auto">
                                <button 
                                    type="submit" 
                                    className="btn btn-primary"
                                    disabled={isLoading}
                                >
                                    {isLoading ? 'Searching...' : 'Search查询'}
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            {isLoading && (
                <div className="text-center my-4">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
            )}

            {traceResult && (
                <div className="card">
                    <div className="card-body">
                        <h3 className="card-title">Trace Result溯源结果</h3>
                        <div className="mb-4">
                            <p><strong>Product商品:</strong> {traceResult.productName}</p>
                            <p><strong>Batch批次号:</strong> {traceResult.batch}</p>
                            <p><strong>Producer生产商:</strong> {traceResult.producer}</p>
                            <p><strong>Production Date生产日期:</strong> {traceResult.productionDate}</p>
                        </div>

                        <h4>Logistics Information物流信息</h4>
                        <div className="timeline">
                            {traceResult.logisticInfo.map((info, index) => (
                                <div key={index} className="card mb-3">
                                    <div className="card-body">
                                        <h5 className="card-title">{info.status}</h5>
                                        <p className="card-text">
                                            <small className="text-muted">
                                                {info.date} - {info.location}
                                            </small>
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Trace; 