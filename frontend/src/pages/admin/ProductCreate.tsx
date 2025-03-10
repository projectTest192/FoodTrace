import React, { useState } from 'react';
import {
    Form,
    Input,
    InputNumber,
    Button,
    Upload,
    Select,
    Modal,
    message
} from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import type { UploadFile } from 'antd/es/upload/interface';

const { TextArea } = Input;
const { Option } = Select;

interface ProductCreateProps {
    visible: boolean;
    onCancel: () => void;
    onSuccess: () => void;
}

const ProductCreate: React.FC<ProductCreateProps> = ({
    visible,
    onCancel,
    onSuccess
}) => {
    const [form] = Form.useForm();
    const [fileList, setFileList] = useState<UploadFile[]>([]);
    const [loading, setLoading] = useState(false);
    const [rfidWaiting, setRfidWaiting] = useState(false);

    const handleSubmit = async (values: any) => {
        setLoading(true);
        try {
            // 这里添加创建商品的API调用
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // 显示RFID等待弹窗
            setRfidWaiting(true);
            
            // 模拟RFID录入过程（5秒后关闭）
            // TODO: 替换为实际的RFID状态轮询
            setTimeout(() => {
                setRfidWaiting(false);
                message.success('商品创建成功！');
                onSuccess();
            }, 5000);
        } catch (error) {
            message.error('创建失败，请重试！');
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <Modal
                title="Create New Product"
                visible={visible}
                onCancel={onCancel}
                footer={null}
                width={800}
            >
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleSubmit}
                >
                    <Form.Item
                        name="name"
                        label="Product Name"
                        rules={[{ required: true }]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        name="description"
                        label="Description"
                        rules={[{ required: true }]}
                    >
                        <TextArea rows={4} />
                    </Form.Item>

                    <Form.Item
                        name="price"
                        label="Price"
                        rules={[{ required: true }]}
                    >
                        <InputNumber
                            min={0}
                            precision={2}
                            style={{ width: '100%' }}
                        />
                    </Form.Item>

                    <Form.Item
                        name="category"
                        label="Category"
                        rules={[{ required: true }]}
                    >
                        <Select>
                            <Option value="fruits">Fruits</Option>
                            <Option value="vegetables">Vegetables</Option>
                            <Option value="meat">Meat</Option>
                            <Option value="seafood">Seafood</Option>
                        </Select>
                    </Form.Item>

                    <Form.Item
                        name="stock"
                        label="Stock"
                        rules={[{ required: true }]}
                    >
                        <InputNumber min={0} style={{ width: '100%' }} />
                    </Form.Item>

                    <Form.Item
                        name="unit"
                        label="Unit"
                        rules={[{ required: true }]}
                    >
                        <Select>
                            <Option value="kg">Kilograms</Option>
                            <Option value="g">Grams</Option>
                            <Option value="piece">Pieces</Option>
                            <Option value="box">Boxes</Option>
                        </Select>
                    </Form.Item>

                    <Form.Item
                        name="expiryDate"
                        label="Expiry Date (Days)"
                        rules={[{ required: true }]}
                    >
                        <InputNumber min={1} style={{ width: '100%' }} />
                    </Form.Item>

                    <Form.Item
                        name="storageCondition"
                        label="Storage Condition"
                        rules={[{ required: true }]}
                    >
                        <Select>
                            <Option value="room">Room Temperature</Option>
                            <Option value="refrigerated">Refrigerated</Option>
                            <Option value="frozen">Frozen</Option>
                        </Select>
                    </Form.Item>

                    <Form.Item
                        name="image"
                        label="Product Image"
                        rules={[{ required: true }]}
                    >
                        <Upload
                            listType="picture-card"
                            fileList={fileList}
                            onChange={({ fileList }) => setFileList(fileList)}
                            beforeUpload={() => false}
                        >
                            {fileList.length < 1 && <PlusOutlined />}
                        </Upload>
                    </Form.Item>

                    <Form.Item>
                        <Button type="primary" htmlType="submit" loading={loading}>
                            Create Product
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>

            <Modal
                title="RFID Registration"
                visible={rfidWaiting}
                footer={null}
                closable={false}
            >
                <div style={{ textAlign: 'center', padding: '20px 0' }}>
                    <p>Waiting for RFID registration...</p>
                    <p>Please wait...</p>
                </div>
            </Modal>
        </>
    );
};

export default ProductCreate; 