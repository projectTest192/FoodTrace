import React, { useState } from 'react';

const QCInspections: React.FC = () => {
    const [activeTab, setActiveTab] = useState('pending');

    return (
        <div className="container mt-4">
            <h2>
                Quality Control Management
                <small className="d-block text-muted">质量检查管理</small>
            </h2>

            {/* 统计卡片 */}
            <div className="row mt-4">
                <div className="col-md-3 mb-3">
                    <div className="card bg-warning text-white">
                        <div className="card-body">
                            <h5 className="card-title">
                                Pending Inspection
                                <small className="d-block">待检查</small>
                            </h5>
                            <h3>15</h3>
                        </div>
                    </div>
                </div>
                <div className="col-md-3 mb-3">
                    <div className="card bg-success text-white">
                        <div className="card-body">
                            <h5 className="card-title">已通过</h5>
                            <h3>128</h3>
                        </div>
                    </div>
                </div>
                <div className="col-md-3 mb-3">
                    <div className="card bg-danger text-white">
                        <div className="card-body">
                            <h5 className="card-title">不合格</h5>
                            <h3>3</h3>
                        </div>
                    </div>
                </div>
                <div className="col-md-3 mb-3">
                    <div className="card bg-info text-white">
                        <div className="card-body">
                            <h5 className="card-title">今日完成</h5>
                            <h3>25</h3>
                        </div>
                    </div>
                </div>
            </div>

            {/* 检查任务列表 */}
            <div className="card mt-4">
                <div className="card-body">
                    <div className="d-flex justify-content-between align-items-center mb-3">
                        <h5 className="card-title">
                            Inspection Tasks
                            <small className="d-block text-muted">检查任务</small>
                        </h5>
                        <button className="btn btn-primary">
                            New Inspection
                            <small className="d-block">新建检查</small>
                        </button>
                    </div>

                    {/* 标签页 */}
                    <ul className="nav nav-tabs mb-3">
                        <li className="nav-item">
                            <button 
                                className={`nav-link ${activeTab === 'pending' ? 'active' : ''}`}
                                onClick={() => setActiveTab('pending')}
                            >
                                待检查
                            </button>
                        </li>
                        <li className="nav-item">
                            <button 
                                className={`nav-link ${activeTab === 'completed' ? 'active' : ''}`}
                                onClick={() => setActiveTab('completed')}
                            >
                                已完成
                            </button>
                        </li>
                        <li className="nav-item">
                            <button 
                                className={`nav-link ${activeTab === 'failed' ? 'active' : ''}`}
                                onClick={() => setActiveTab('failed')}
                            >
                                不合格
                            </button>
                        </li>
                    </ul>

                    {/* 任务列表 */}
                    <table className="table">
                        <thead>
                            <tr>
                                <th>批次号</th>
                                <th>商品名称</th>
                                <th>生产日期</th>
                                <th>检查项目</th>
                                <th>状态</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>QC20240118001</td>
                                <td>有机蔬菜</td>
                                <td>2024-01-18</td>
                                <td>农残检测</td>
                                <td>
                                    <span className="badge bg-warning">待检查</span>
                                </td>
                                <td>
                                    <button className="btn btn-sm btn-primary me-2">开始检查</button>
                                    <button className="btn btn-sm btn-info">查看详情</button>
                                </td>
                            </tr>
                            <tr>
                                <td>QC20240118002</td>
                                <td>水果套装</td>
                                <td>2024-01-18</td>
                                <td>品质检验</td>
                                <td>
                                    <span className="badge bg-success">已通过</span>
                                </td>
                                <td>
                                    <button className="btn btn-sm btn-info me-2">查看报告</button>
                                    <button className="btn btn-sm btn-success">导出PDF</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            {/* 检查表单模态框 */}
            <div className="modal fade" id="inspectionModal">
                <div className="modal-dialog modal-lg">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title">质量检查表单</h5>
                            <button type="button" className="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div className="modal-body">
                            <form>
                                <div className="mb-3">
                                    <label className="form-label">检查项目</label>
                                    <div className="form-check">
                                        <input type="checkbox" className="form-check-input" id="check1" />
                                        <label className="form-check-label">外观检查</label>
                                    </div>
                                    <div className="form-check">
                                        <input type="checkbox" className="form-check-input" id="check2" />
                                        <label className="form-check-label">农残检测</label>
                                    </div>
                                    <div className="form-check">
                                        <input type="checkbox" className="form-check-input" id="check3" />
                                        <label className="form-check-label">包装完整性</label>
                                    </div>
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">检查结果</label>
                                    <textarea className="form-control" rows={3}></textarea>
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">图片上传</label>
                                    <input type="file" className="form-control" multiple />
                                </div>
                            </form>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                            <button type="button" className="btn btn-success">通过</button>
                            <button type="button" className="btn btn-danger">不合格</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default QCInspections; 