import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Steps, Descriptions, Tag, Timeline, Row, Col } from 'antd';
import { EnvironmentOutlined, CloudOutlined, HistoryOutlined } from '@ant-design/icons';
import AMapLoader from '@amap/amap-jsapi-loader';
import { Product } from '../../types';

// 修改模拟数据，基于牛津布鲁克斯大学场景
const mockTraceData = {
  id: "PROD001",
  name: "Fresh Meal Box",
  description: "Fresh prepared meals from OBU Food Science Lab",
  producer: "OBU Food Science Lab - Gibbs Building",
  productDate: "2024-03-15",
  status: "active",
  deviceId: "OBU_GIBBS_001",
  rfidId: "RFID_OBU001",
  temperature: 4.5,
  humidity: 45.2,
  // Gibbs Building coordinates
  latitude: 51.755234,
  longitude: -1.224377,
  writeTime: "2024-03-15T10:30:00Z",
  // 配送信息
  shipment: {
    startTime: "2024-03-15T14:00:00Z",
    endTime: "2024-03-15T16:30:00Z",
    from: "Gibbs Building - Food Science Laboratory",
    to: "John Henry Brookes Building - University Food Court",
    transportData: [
      {
        // Starting from Gibbs Building
        time: "2024-03-15T14:00:00Z",
        temperature: 4.3,
        humidity: 46.0,
        location: { lat: 51.755234, lng: -1.224377 }
      },
      {
        // Moving through Headington Campus Square
        time: "2024-03-15T14:30:00Z",
        temperature: 4.3,
        humidity: 46.0,
        location: { lat: 51.754847, lng: -1.223824 }
      },
      {
        // Distribution Centre Check
        time: "2024-03-15T15:00:00Z",
        temperature: 4.4,
        humidity: 45.9,
        location: { lat: 51.754440, lng: -1.223481 }
      },
      {
        // Moving towards JHBB
        time: "2024-03-15T15:30:00Z",
        temperature: 4.4,
        humidity: 45.8,
        location: { lat: 51.753901, lng: -1.223749 }
      },
      {
        // Approaching JHBB
        time: "2024-03-15T16:00:00Z",
        temperature: 4.5,
        humidity: 45.7,
        location: { lat: 51.753538, lng: -1.224001 }
      },
      {
        // Arriving at JHBB Food Court
        time: "2024-03-15T16:30:00Z",
        temperature: 4.5,
        humidity: 45.7,
        location: { lat: 51.753228, lng: -1.224184 }
      }
    ]
  }
};

const ProductTrace: React.FC = () => {
  const { productId } = useParams<{ productId: string }>();
  const [traceData, setTraceData] = useState(mockTraceData);
  const [map, setMap] = useState<any>(null);

  useEffect(() => {
    initMap();
  }, []);

  const initMap = async () => {
    try {
      const AMap = await AMapLoader.load({
        key: 'your-amap-key', // 替换为你的高德地图 key
        version: '2.0',
        plugins: ['AMap.PolyLine', 'AMap.Marker']
      });

      const map = new AMap.Map('container', {
        zoom: 13,
        center: [traceData.shipment.transportData[0].location.lng, 
                  traceData.shipment.transportData[0].location.lat] // 初始中心点
      });

      // 创建起点标记
      const startMarker = new AMap.Marker({
        position: [traceData.shipment.transportData[0].location.lng, 
                  traceData.shipment.transportData[0].location.lat],
        title: 'Start Point'
      });

      // 创建终点标记
      const endMarker = new AMap.Marker({
        position: [traceData.shipment.transportData[traceData.shipment.transportData.length - 1].location.lng,
                  traceData.shipment.transportData[traceData.shipment.transportData.length - 1].location.lat],
        title: 'End Point'
      });

      // 创建路径线条
      const path = traceData.shipment.transportData.map(point => [
        point.location.lng,
        point.location.lat
      ]);

      const polyline = new AMap.Polyline({
        path: path,
        strokeColor: '#3366FF',
        strokeWeight: 6,
        strokeOpacity: 0.8
      });

      map.add([startMarker, endMarker, polyline]);
      map.setFitView();

      setMap(map);
    } catch (error) {
      console.error('Failed to load map:', error);
    }
  };

  return (
    <div className="container mt-4">
      <h2>Product Traceability Information</h2>
      
      {/* 商品基本信息 */}
      <Card title="Basic Information" className="mb-4">
        <Descriptions bordered>
          <Descriptions.Item label="Product ID">{traceData.id}</Descriptions.Item>
          <Descriptions.Item label="Name">{traceData.name}</Descriptions.Item>
          <Descriptions.Item label="Producer">{traceData.producer}</Descriptions.Item>
          <Descriptions.Item label="Production Date">{traceData.productDate}</Descriptions.Item>
          <Descriptions.Item label="RFID Code">{traceData.rfidId}</Descriptions.Item>
          <Descriptions.Item label="Status">
            <Tag color={traceData.status === 'active' ? 'green' : 'default'}>
              {traceData.status === 'active' ? 'Active' : 'Sold'}
            </Tag>
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {/* 生产环境数据 */}
      <Card title="Production Environment Data" className="mb-4">
        <Row gutter={16}>
          <Col span={8}>
            <Card type="inner" title="Temperature">
              <CloudOutlined style={{ fontSize: 24, color: '#1890ff' }} />
              <h3>{traceData.temperature}°C</h3>
            </Card>
          </Col>
          <Col span={8}>
            <Card type="inner" title="Humidity">
              <CloudOutlined style={{ fontSize: 24, color: '#52c41a' }} />
              <h3>{traceData.humidity}%</h3>
            </Card>
          </Col>
          <Col span={8}>
            <Card type="inner" title="Location">
              <EnvironmentOutlined style={{ fontSize: 24, color: '#f5222d' }} />
              <p>Oxford Brookes University</p>
            </Card>
          </Col>
        </Row>
      </Card>

      {/* 配送追踪 */}
      <Card title="Logistics Tracking" className="mb-4">
        <Timeline mode="left">
          <Timeline.Item dot={<HistoryOutlined />}>
            Production Completed
            <p>{traceData.writeTime}</p>
            <p>Temperature: {traceData.temperature}°C</p>
          </Timeline.Item>
          {traceData.shipment.transportData.map((data, index) => (
            <Timeline.Item key={index}>
              Transport Check Point {index + 1}
              <p>{data.time}</p>
              <p>Temperature: {data.temperature}°C</p>
              <p>Humidity: {data.humidity}%</p>
            </Timeline.Item>
          ))}
          <Timeline.Item>
            Delivery Completed
            <p>{traceData.shipment.endTime}</p>
          </Timeline.Item>
        </Timeline>
      </Card>

      {/* 添加地图组件 */}
      <Card title="Logistics Route" className="mb-4">
        <div id="container" style={{ height: '400px', width: '100%' }}>
          {/* 地图将在这里渲染 */}
        </div>
      </Card>

      {/* 区块链信息 */}
      <Card title="Blockchain Information">
        <Descriptions bordered column={1}>
          <Descriptions.Item label="Device ID">{traceData.deviceId}</Descriptions.Item>
          <Descriptions.Item label="RFID ID">{traceData.rfidId}</Descriptions.Item>
          <Descriptions.Item label="Write Time">{traceData.writeTime}</Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
};

const ProductDetail: React.FC<{ product: Product }> = ({ product }) => (
  <Card>
    <Descriptions title="Location Details" bordered>
      <Descriptions.Item label="Production Site">
        Gibbs Building - Food Science Laboratory
      </Descriptions.Item>
      <Descriptions.Item label="Distribution Centre">
        Headington Campus Square
      </Descriptions.Item>
      <Descriptions.Item label="Retail Location">
        John Henry Brookes Building - Food Court
      </Descriptions.Item>
    </Descriptions>
  </Card>
);

export default ProductTrace; 