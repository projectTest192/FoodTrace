import React, { useState, ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { createEnterpriseUser } from '../api/admin';

const Admin: React.FC = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        pwd: '',
        role: 'producer' as const,
        phone: ''
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            await createEnterpriseUser(formData);
            setSuccess('企业用户创建成功！');
            setFormData({
                name: '',
                email: '',
                pwd: '',
                role: 'producer',
                phone: ''
            });
        } catch (err) {
            setError('创建失败，请重试');
            console.error(err);
        }
    };

    const handleInputChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-md-8">
                    <div className="card">
                        <div className="card-header d-flex justify-content-between align-items-center">
                            <h3 className="mb-0">创建企业用户</h3>
                            <button 
                                className="btn btn-outline-danger"
                                onClick={() => navigate('/')}
                            >
                                返回
                            </button>
                        </div>
                        <div className="card-body">
                            {error && (
                                <div className="alert alert-danger">{error}</div>
                            )}
                            {success && (
                                <div className="alert alert-success">{success}</div>
                            )}
                            <form onSubmit={handleSubmit}>
                                <div className="mb-3">
                                    <label className="form-label">用户名</label>
                                    <input
                                        name="name"
                                        type="text"
                                        className="form-control"
                                        value={formData.name}
                                        onChange={handleInputChange}
                                        required
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">邮箱</label>
                                    <input
                                        name="email"
                                        type="email"
                                        className="form-control"
                                        value={formData.email}
                                        onChange={handleInputChange}
                                        required
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">密码</label>
                                    <input
                                        name="pwd"
                                        type="password"
                                        className="form-control"
                                        value={formData.pwd}
                                        onChange={handleInputChange}
                                        required
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">手机号</label>
                                    <input
                                        name="phone"
                                        type="tel"
                                        className="form-control"
                                        value={formData.phone}
                                        onChange={handleInputChange}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">用户角色</label>
                                    <select
                                        name="role"
                                        className="form-control"
                                        value={formData.role}
                                        onChange={handleInputChange}
                                    >
                                        <option value="producer">生产商</option>
                                        <option value="distributor">配送商</option>
                                        <option value="retailer">零售商</option>
                                    </select>
                                </div>
                                <button type="submit" className="btn btn-primary">
                                    创建用户
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Admin; 