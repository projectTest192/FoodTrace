import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { message } from 'antd';

interface RegisterData {
    name: string;
    email: string;
    pwd: string;
    role_id: number;
    // 企业用户额外信息
    bizLic?: string;
    addr?: string;
    contName?: string;
    contPhone?: string;
}

const Register: React.FC = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState<RegisterData>({
        name: '',
        email: '',
        pwd: '',
        role_id: 5 // 默认为消费者
    });
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            let endpoint = 'consumer';
            let data = formData;

            // 根据角色选择不同的注册端点
            switch (formData.role_id) {
                case 2: // 生产商
                    endpoint = 'producer';
                    break;
                case 3: // 经销商
                    endpoint = 'distributor';
                    break;
                case 4: // 零售商
                    endpoint = 'retailer';
                    break;
                default: // 消费者
                    endpoint = 'consumer';
            }

            await axios.post(
                `http://localhost:8002/api/auth/register/${endpoint}`,
                data
            );

            message.success('Registration successful! Please check your email for verification.');
            navigate('/auth');
        } catch (error: any) {
            if (error.response?.data?.detail) {
                message.error(error.response.data.detail);
            } else {
                message.error('Registration failed');
            }
        } finally {
            setIsLoading(false);
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h2>Register</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Name</label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleInputChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleInputChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            name="pwd"
                            value={formData.pwd}
                            onChange={handleInputChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Role</label>
                        <select 
                            name="role_id" 
                            value={formData.role_id}
                            onChange={handleInputChange}
                            required
                        >
                            <option value="5">Consumer</option>
                            <option value="2">Producer</option>
                            <option value="3">Distributor</option>
                            <option value="4">Retailer</option>
                        </select>
                    </div>

                    {/* 企业用户额外信息 */}
                    {formData.role_id !== 5 && (
                        <>
                            <div className="form-group">
                                <label>Business License</label>
                                <input
                                    type="text"
                                    name="bizLic"
                                    value={formData.bizLic || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Address</label>
                                <input
                                    type="text"
                                    name="addr"
                                    value={formData.addr || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Contact Name</label>
                                <input
                                    type="text"
                                    name="contName"
                                    value={formData.contName || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Contact Phone</label>
                                <input
                                    type="text"
                                    name="contPhone"
                                    value={formData.contPhone || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </div>
                        </>
                    )}

                    <button 
                        type="submit" 
                        disabled={isLoading}
                        className="login-button"
                    >
                        {isLoading ? 'Registering...' : 'Register'}
                    </button>
                </form>
                <p className="register-link">
                    Already have an account? <a href="/auth">Login here</a>
                </p>
            </div>
        </div>
    );
};

export default Register; 