import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
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
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// 注册 Chart.js 组件
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

interface HistoricalData {
    deviceId: string;
    timestamp: string;
    temperature: number;
    humidity: number;
}

interface IoTData {
    deviceId: string;
    productName: string;
    timestamp: string;
    temperature: number;
    humidity: number;
    location: string;
    coordinates: {
        latitude: number;
        longitude: number;
    };
}

// 模拟历史数据
const generateHistoricalData = (deviceId: string, hours: number): HistoricalData[] => {
    const data: HistoricalData[] = [];
    const now = new Date();
    for (let i = hours; i >= 0; i--) {
        const time = new Date(now.getTime() - i * 3600000);
        data.push({
            deviceId,
            timestamp: time.toISOString(),
            temperature: 4 + Math.random() * 2,
            humidity: 45 + Math.random() * 10
        });
    }
    return data;
};

const mockDevices: IoTData[] = [
    {
        deviceId: "DEV001",
        productName: "Fresh Food Package",
        timestamp: "2024-01-18T10:30:00",
        temperature: 4.5,
        humidity: 45,
        location: "Headington Campus - Gibbs Building Lab",
        coordinates: {
            latitude: 51.755234,
            longitude: -1.224377
        }
    },
    {
        deviceId: "DEV002",
        productName: "Organic Meal Box",
        timestamp: "2024-01-18T10:30:00",
        temperature: 5.2,
        humidity: 48,
        location: "Headington Campus - Food Science Center",
        coordinates: {
            latitude: 51.754847,
            longitude: -1.223824
        }
    }
];

const Monitor: React.FC = () => {
    const [devices, setDevices] = useState<IoTData[]>([]);
    const [historicalData, setHistoricalData] = useState<HistoricalData[]>([]);
    const [expandedDevice, setExpandedDevice] = useState<string | null>(null);
    const [currentLocation, setCurrentLocation] = useState<{latitude: number; longitude: number} | null>(null);

    // 获取当前位置
    useEffect(() => {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    setCurrentLocation({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    });
                },
                (error) => {
                    console.error("Error getting location:", error);
                }
            );
        } else {
            console.log("Geolocation is not supported by this browser.");
        }
    }, []);

    useEffect(() => {
        // 模拟实时数据更新
        const fetchData = () => {
            const updatedDevices = mockDevices.map(device => ({
                ...device,
                timestamp: new Date().toISOString(),
                temperature: device.temperature + (Math.random() - 0.5),
                humidity: device.humidity + (Math.random() - 0.5) * 2,
                // 如果有当前位置，则使用当前位置
                coordinates: currentLocation || device.coordinates
            }));
            setDevices(updatedDevices);
        };

        fetchData();
        const interval = setInterval(fetchData, 5000);

        // 获取历史数据
        const allHistoricalData = mockDevices.flatMap(device => 
            generateHistoricalData(device.deviceId, 24).map((data: HistoricalData) => ({
                ...data,
                productName: device.productName
            }))
        );
        setHistoricalData(allHistoricalData);

        return () => clearInterval(interval);
    }, [currentLocation]);  // 添加 currentLocation 作为依赖

    const config = {
        data: historicalData.filter(data => data.deviceId === expandedDevice),
        height: 300,
        xField: 'timestamp',
        yField: 'temperature',
        point: {
            size: 5,
            shape: 'diamond',
        },
        tooltip: {
            formatter: (datum: any) => {
                return { name: 'Temperature', value: `${datum.temperature.toFixed(1)}°C` };
            },
        },
    };

    // 修改图表配置
    const chartData = {
        labels: historicalData
            .filter(data => data.deviceId === expandedDevice)
            .map(data => new Date(data.timestamp).toLocaleTimeString()),
        datasets: [
            {
                label: 'Temperature (°C)',
                data: historicalData
                    .filter(data => data.deviceId === expandedDevice)
                    .map(data => data.temperature),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }
        ]
    };

    const chartOptions = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top' as const,
            },
            title: {
                display: true,
                text: 'Temperature History温度历史'
            }
        },
        scales: {
            y: {
                beginAtZero: false,
                title: {
                    display: true,
                    text: 'Temperature (°C)'
                }
            }
        }
    };

    return (
        <div className="container">
            <h2 className="mb-4">Product IoT Monitor商品物联监控</h2>
            
            <div className="row">
                {devices.map(device => (
                    <div key={device.deviceId} className="col-md-6 mb-4">
                        <div className="card">
                            <div className="card-header d-flex justify-content-between align-items-center">
                                <h5 className="mb-0">{device.productName}</h5>
                                <button 
                                    className="btn btn-link"
                                    onClick={() => setExpandedDevice(
                                        expandedDevice === device.deviceId ? null : device.deviceId
                                    )}
                                >
                                    {expandedDevice === device.deviceId ? '收起' : '展开'}
                                </button>
                            </div>
                            <div className="card-body">
                                <div className="mb-3">
                                    <small className="text-muted">Device ID设备ID:</small>
                                    <div>{device.deviceId}</div>
                                </div>
                                <div className="mb-3">
                                    <small className="text-muted">Location位置:</small>
                                    <div>{device.location}</div>
                                </div>
                                <div className="mb-3">
                                    <small className="text-muted">Last Update最后更新:</small>
                                    <div>{new Date(device.timestamp).toLocaleString()}</div>
                                </div>
                                <div className="row">
                                    <div className="col-6">
                                        <div className="text-center">
                                            <div className="h4 mb-0">
                                                {device.temperature.toFixed(1)}°C
                                            </div>
                                            <small className="text-muted">Temperature温度</small>
                                        </div>
                                    </div>
                                    <div className="col-6">
                                        <div className="text-center">
                                            <div className="h4 mb-0">
                                                {device.humidity.toFixed(1)}%
                                            </div>
                                            <small className="text-muted">Humidity湿度</small>
                                        </div>
                                    </div>
                                </div>

                                {expandedDevice === device.deviceId && (
                                    <>
                                        <div className="mt-4">
                                            <h6>Temperature History温度历史</h6>
                                            <Line data={chartData} options={chartOptions} />
                                        </div>
                                        <div className="mt-4">
                                            <h6>Location Map位置地图</h6>
                                            {currentLocation ? (
                                                <div style={{ height: '300px', width: '100%', marginTop: '1rem' }}>
                                                    <MapContainer 
                                                        center={[currentLocation.latitude, currentLocation.longitude]} 
                                                        zoom={13} 
                                                        style={{ height: '100%', width: '100%' }}
                                                    >
                                                        <TileLayer
                                                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                                                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                                                        />
                                                        <Marker position={[currentLocation.latitude, currentLocation.longitude]}>
                                                            <Popup>
                                                                <strong>{device.productName}</strong><br />
                                                                Current Location当前位置<br />
                                                                Lat: {currentLocation.latitude.toFixed(4)}<br />
                                                                Lng: {currentLocation.longitude.toFixed(4)}
                                                            </Popup>
                                                        </Marker>
                                                    </MapContainer>
                                                </div>
                                            ) : (
                                                <div className="alert alert-info">
                                                    Getting current location...获取当前位置中...
                                                </div>
                                            )}
                                        </div>
                                    </>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Monitor; 