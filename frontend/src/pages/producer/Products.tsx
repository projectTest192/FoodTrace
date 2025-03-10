import React, { useState, useEffect } from 'react';
import { Button, Card, Table, Modal, Form, Input, DatePicker, message, Select, Spin, Descriptions } from 'antd';
import { PlusOutlined, LoadingOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import moment from 'moment';
import api, { producerAPI } from '../../services/api';

interface Product {
  id: number;
  name: string;
  description: string;
  category_id: number;
  batch_no: string;
  production_date: string;
  shelf_life: number;
  price: number;
  status: string;
  rfid_code?: string;
  factory_data?: {
    temperature: number;
    humidity: number;
    latitude: number;
    longitude: number;
    device_id: string;
  };
}

interface Category {
  id: number;
  name: string;
}

interface StatusMapType {
  [key: string]: string;
}

interface ProductResponse {
  id: number;
  status: string;
}

interface ProductData {
  status: string;
  // ... 其他产品数据字段
}

const statusMap: StatusMapType = {
  created: 'Pending RFID',
  active: 'Active',
  inTransit: 'In Transit',
  sold: 'Sold'
};

const mockProducts = [
  {
    id: 'PROD001',
    name: 'Fresh Meal Box',
    description: 'Daily prepared fresh meals for students and staff',
    category: 'Ready Meals',
    batch_no: 'GB24031501',
    production_date: '2024-03-15',
    status: 'created',
    lab_location: 'Gibbs Building Lab 2.1',
    supervisor: 'Dr. Smith'
  },
  {
    id: 'PROD002',
    name: 'Sandwich Pack',
    description: 'Freshly made sandwiches from OBU kitchen',
    category: 'Sandwiches',
    batch_no: 'GB24031502',
    production_date: '2024-03-15',
    status: 'active',
    lab_location: 'Gibbs Building Lab 2.2',
    supervisor: 'Dr. Johnson'
  }
];

const mockCategories = [
  { id: 1, name: 'Ready Meals' },
  { id: 2, name: 'Sandwiches' },
  { id: 3, name: 'Salads' },
  { id: 4, name: 'Beverages' }
];

const ProducerProducts: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isRFIDModalVisible, setIsRFIDModalVisible] = useState(false);
  const [currentProduct, setCurrentProduct] = useState<Product | null>(null);
  const [form] = Form.useForm();
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false);
  const [detailVisible, setDetailVisible] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [loadingText, setLoadingText] = useState('');

  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await fetch('/api/products');
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      message.error('Failed to fetch products');
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch('/api/categories');
      const data = await response.json();
      setCategories(data);
    } catch (error) {
      message.error('获取分类列表失败');
    }
  };

  const columns: ColumnsType<Product> = [
    {
      title: 'Product Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Batch No.',
      dataIndex: 'batch_no',
      key: 'batch_no',
    },
    {
      title: 'Production Date',
      dataIndex: 'production_date',
      key: 'production_date',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        return statusMap[status] || status;
      }
    },
    {
      title: 'Actions',
      key: 'action',
      render: (_, record) => (
        <span>
          {record.status === 'created' && (
            <Button type="link" onClick={() => handleRFIDBinding(record)}>
              Bind RFID
            </Button>
          )}
          <Button type="link" onClick={() => viewDetails(record)}>
            View Details
          </Button>
        </span>
      ),
    },
  ];

  const handleCreate = async (values: any) => {
    try {
      // 调用创建产品API
      const response = await api.post<ProductResponse>('/products', values);
      const { id, status } = response.data;
      
      if (status === 'waiting_rfid') {
        setLoading(true);
        setLoadingText('Waiting for RFID input...');
        
        // 2. 轮询检查状态
        const checkStatus = setInterval(async () => {
          const { data } = await api.get<ProductData>(`/products/${id}`);
          if (data.status === 'active') {
            clearInterval(checkStatus);
            setLoading(false);
            message.success('Product created successfully!');
            fetchProducts();
          }
        }, 3000);
        
        // 3. 设置超时
        setTimeout(() => {
          clearInterval(checkStatus);
          setLoading(false);
          message.error('RFID input timeout, please try again');
        }, 60000);
      }
    } catch (error) {
      setLoading(false);
      message.error('Failed to create product');
    }
  };

  const handleRFIDBinding = async (product: Product) => {
    setCurrentProduct(product);
    setIsRFIDModalVisible(true);
    try {
      // 发送请求到树莓派
      const response = await fetch('http://raspberry-pi-ip:port/write-rfid', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          productId: product.id,
          productData: {
            name: product.name,
            batch_no: product.batch_no,
            production_date: product.production_date
          }
        }),
      });

      if (response.ok) {
        const { rfid_code, sensor_data } = await response.json();
        // 更新产品信息
        await updateProductWithIoTData(product.id, rfid_code, sensor_data);
      }
    } catch (error) {
      message.error('RFID写入失败');
    }
  };

  const updateProductWithIoTData = async (productId: number, rfidCode: string, sensorData: any) => {
    try {
      const response = await fetch(`/api/products/${productId}/factory-data`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rfid_code: rfidCode,
          factory_data: sensorData
        }),
      });

      if (response.ok) {
        message.success('产品信息更新成功');
        fetchProducts(); // 刷新产品列表
        setIsRFIDModalVisible(false);
      }
    } catch (error) {
      message.error('更新产品信息失败');
    }
  };

  const viewDetails = (product: Product) => {
    setSelectedProduct(product);
    setDetailVisible(true);
  };

  // 创建产品表单
  const createProductForm = (
    <Form form={form} onFinish={handleCreate} layout="vertical">
      <Form.Item
        name="name"
        label="Product Name"
        rules={[{ required: true, message: 'Please input product name' }]}
      >
        <Input />
      </Form.Item>
      <Form.Item
        name="description"
        label="Description"
      >
        <Input.TextArea />
      </Form.Item>
      <Form.Item
        name="category_id"
        label="Product Category"
        rules={[{ required: true, message: 'Please select product category' }]}
      >
        <Select>
          {categories.map(cat => (
            <Select.Option key={cat.id} value={cat.id}>{cat.name}</Select.Option>
          ))}
        </Select>
      </Form.Item>
      <Form.Item
        name="batch_no"
        label="Batch No."
        rules={[{ required: true, message: 'Please input batch no.' }]}
      >
        <Input />
      </Form.Item>
      <Form.Item
        name="production_date"
        label="Production Date"
        rules={[{ required: true, message: 'Please select production date' }]}
      >
        <DatePicker />
      </Form.Item>
      <Form.Item
        name="shelf_life"
        label="Shelf Life (Days)"
        rules={[{ required: true, message: 'Please input shelf life' }]}
      >
        <Input type="number" />
      </Form.Item>
      <Form.Item
        name="price"
        label="Price"
        rules={[{ required: true, message: 'Please input price' }]}
      >
        <Input type="number" step="0.01" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          Create Product
        </Button>
      </Form.Item>
    </Form>
  );

  // 产品详情展示
  const ProductDetail: React.FC<{ product: Product }> = ({ product }) => (
    <Card>
      <Descriptions title="Product Details" bordered>
        <Descriptions.Item label="Product Name">{product.name}</Descriptions.Item>
        <Descriptions.Item label="Batch No.">
          {product.batch_no}
        </Descriptions.Item>
        <Descriptions.Item label="Production Date">
          {moment(product.production_date).format('YYYY-MM-DD')}
        </Descriptions.Item>
        {product.factory_data && (
          <>
            <Descriptions.Item label="Factory Temperature">
              {product.factory_data.temperature}°C
            </Descriptions.Item>
            <Descriptions.Item label="Factory Humidity">
              {product.factory_data.humidity}%
            </Descriptions.Item>
            <Descriptions.Item label="RFID Code">
              {product.rfid_code}
            </Descriptions.Item>
          </>
        )}
      </Descriptions>
    </Card>
  );

  return (
    <div className="p-6">
      <div className="mb-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">Product Management</h1>
        <Button 
          type="primary" 
          icon={<PlusOutlined />}
          onClick={() => setIsModalVisible(true)}
        >
          Create Product
        </Button>
      </div>

      <Table columns={columns} dataSource={products} />

      {/* 创建产品表单 */}
      <Modal
        title="Create New Product"
        visible={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
      >
        {createProductForm}
      </Modal>

      {/* RFID绑定弹窗 */}
      <Modal
        title="RFID Binding"
        visible={isRFIDModalVisible}
        onCancel={() => setIsRFIDModalVisible(false)}
        footer={null}
      >
        <div className="text-center">
          <p>Please place RFID tag near the reader</p>
          <p>{loadingText}</p>
          {/* 可以添加loading动画 */}
        </div>
      </Modal>

      {/* 详情弹窗 */}
      <Modal
        title="Product Details"
        visible={detailVisible}
        onCancel={() => setDetailVisible(false)}
        footer={null}
        width={800}
      >
        {selectedProduct && <ProductDetail product={selectedProduct} />}
      </Modal>
    </div>
  );
};

export default ProducerProducts; 