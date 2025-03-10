import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// 注册 ChartJS 组件
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

// 图表数据
const tempData = {
    labels: ['12:00', '13:00', '14:00', '15:00', '16:00'],
    datasets: [
        {
            label: 'Temperature °C',
            data: [4, 5, 8, 7, 6],
            borderColor: 'rgb(255, 99, 132)',
            tension: 0.1,
        },
    ],
};

const humidityData = {
    labels: ['12:00', '13:00', '14:00', '15:00', '16:00'],
    datasets: [
        {
            label: 'Humidity %',
            data: [45, 48, 50, 46, 47],
            borderColor: 'rgb(53, 162, 235)',
            tension: 0.1,
        },
    ],
};

const SupervisorOverview: React.FC = () => {
    return (
        <div className="container mt-4">
            <h2>
                Supervision Overview
                <small className="d-block text-muted">监管概览</small>
            </h2>

            {/* 实时监控数据 */}
            <div className="row mt-4">
                <div className="col-md-3 mb-3">
                    <div className="card bg-primary text-white">
                        <div className="card-body">
                            <h5 className="card-title">
                                Active Products
                                <small className="d-block">在监商品</small>
                            </h5>
                            <h3>1,234</h3>
                        </div>
                    </div>
                </div>
                <div className="col-md-3 mb-3">
                    <div className="card bg-warning text-white">
                        <div className="card-body">
                            <h5 className="card-title">
                                Alerts Today
                                <small className="d-block">今日预警</small>
                            </h5>
                            <h3>5</h3>
                        </div>
                    </div>
                </div>
                <div className="col-md-3 mb-3">
                    <div className="card bg-success text-white">
                        <div className="card-body">
                            <h5 className="card-title">
                                Compliance Rate
                                <small className="d-block">合规率</small>
                            </h5>
                            <h3>98.5%</h3>
                        </div>
                    </div>
                </div>
                <div className="col-md-3 mb-3">
                    <div className="card bg-info text-white">
                        <div className="card-body">
                            <h5 className="card-title">
                                Active Sensors
                                <small className="d-block">在线传感器</small>
                            </h5>
                            <h3>56</h3>
                        </div>
                    </div>
                </div>
            </div>

            {/* 温度湿度监控 */}
            <div className="row mt-4">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h5 className="card-title">
                                Temperature Monitoring
                                <small className="d-block text-muted">温度监控</small>
                            </h5>
                            <div style={{ height: '300px' }}>
                                <Line data={tempData} />
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h5 className="card-title">
                                Humidity Monitoring
                                <small className="d-block text-muted">湿度监控</small>
                            </h5>
                            <div style={{ height: '300px' }}>
                                <Line data={humidityData} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* 预警信息列表 */}
            <div className="card mt-4">
                <div className="card-body">
                    <h5 className="card-title">
                        Alert Messages
                        <small className="d-block text-muted">预警信息</small>
                    </h5>
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Time 时间</th>
                                <th>Type 类型</th>
                                <th>Location 位置</th>
                                <th>Description 描述</th>
                                <th>Status 状态</th>
                                <th>Actions 操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>2024-01-18 14:30</td>
                                <td>
                                    <span className="badge bg-danger">Temperature Alert 温度预警</span>
                                </td>
                                <td>Storage A-01</td>
                                <td>Temperature exceeds threshold (&gt;8°C)</td>
                                <td>
                                    <span className="badge bg-warning">Pending 待处理</span>
                                </td>
                                <td>
                                    <button className="btn btn-sm btn-primary me-2">Handle 处理</button>
                                    <button className="btn btn-sm btn-info">Details 详情</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            {/* 合规报告 */}
            <div className="card mt-4">
                <div className="card-body">
                    <h5 className="card-title">
                        Compliance Reports
                        <small className="d-block text-muted">合规报告</small>
                    </h5>
                    <div className="list-group">
                        <a href="#" className="list-group-item list-group-item-action">
                            <div className="d-flex w-100 justify-content-between">
                                <h6 className="mb-1">Monthly Compliance Report 月度合规报告</h6>
                                <small>2024-01</small>
                            </div>
                            <p className="mb-1">Overall compliance rate: 98.5% 总体合规率：98.5%</p>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SupervisorOverview; 