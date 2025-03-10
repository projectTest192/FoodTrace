import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { message } from 'antd';

// 定义响应数据的接口
interface LoginResponse {
    accToken: string;
    tokenType: string;
    user: {
        id: string;
        email: string;
        role: string;
        verified: boolean;
    };
}

const Login: React.FC = () => {
    const [formData, setFormData] = useState({
        email: '',
        pwd: ''
    });
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const response = await axios.post<LoginResponse>(
                'http://localhost:8002/api/auth/login', 
                formData
            );
            
            const { accToken, user } = response.data;
            
            // 保存登录信息
            localStorage.setItem('token', accToken);
            localStorage.setItem('userRole', user.role);
            localStorage.setItem('userEmail', user.email);
            
            // 根据角色重定向
            switch (user.role) {
                case 'admin':
                    navigate('/admin/dashboard');
                    break;
                case 'producer':
                    navigate('/producer/products');
                    break;
                case 'distributor':
                    navigate('/distributor/shipments');
                    break;
                case 'retailer':
                    navigate('/retailer/products');
                    break;
                case 'consumer':
                    navigate('/consumer/products');
                    break;
                default:
                    message.error('Unknown user role');
            }
        } catch (error: any) {
            if (error.response?.data?.detail) {
                message.error(error.response.data.detail);
            } else {
                message.error('Login failed');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            value={formData.email}
                            onChange={e => setFormData({...formData, email: e.target.value})}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            value={formData.pwd}
                            onChange={e => setFormData({...formData, pwd: e.target.value})}
                            required
                        />
                    </div>
                    <button 
                        type="submit" 
                        disabled={isLoading}
                        className="login-button"
                    >
                        {isLoading ? 'Logging in...' : 'Login'}
                    </button>
                </form>
                <p className="register-link">
                    Don't have an account? <a href="/register">Register here</a>
                </p>
                
                <div className="privacy-notice mt-4 p-3 bg-light rounded">
                    <h6 className="text-muted">Privacy Policy</h6>
                    <p className="small text-muted mb-2">
                        Our Food Traceability System strictly adheres to the GDPR (EU 2016/679).
                    </p>
                    <ul className="small text-muted ps-3">
                        <li>User emails and phone numbers are encrypted and stored securely off-chain.</li>
                        <li>Access controlled through JWT tokens and Role-Based Access Control (RBAC).</li>
                        <li>Detailed policy is available <a href="/privacy-policy" className="text-primary">here</a>.</li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default Login; 