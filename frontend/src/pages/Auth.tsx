import React, { useState, ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, register } from '../api/auth';
import '../styles/auth.css';

const Auth: React.FC = () => {
    const navigate = useNavigate();
    const [isLogin, setIsLogin] = useState(true);
    const [error, setError] = useState<string>('');
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        pwd: '',
        phone: '',
        role: ''
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        try {
            if (isLogin) {
                const response = await login({
                    email: formData.email,
                    pwd: formData.pwd
                });
                if (response.accToken) {
                    localStorage.setItem('token', response.accToken);
                    localStorage.setItem('userRole', response.user.role);
                    
                    // 根据角色跳转到不同页面
                    switch (response.user.role) {
                        case 'admin':
                            navigate('/admin/dashboard');
                            break;
                        case 'consumer':
                            navigate('/consumer/products');
                            break;
                        case 'producer':
                            navigate('/producer/products');
                            break;
                        case 'storage':
                            navigate('/storage/inventory');
                            break;
                        case 'qc':
                            navigate('/qc/inspections');
                            break;
                        case 'supervisor':
                            navigate('/supervisor/overview');
                            break;
                        default:
                            setError('Unknown user role');
                    }
                }
            } else {
                const registerData = {
                    name: formData.name,
                    email: formData.email,
                    pwd: formData.pwd,
                    phone: formData.phone
                };
                await register(registerData);
                setError('Registration successful! Please check your email for verification.');
                setIsLogin(true);
            }
        } catch (err) {
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError('Operation failed, please try again');
            }
        }
    };

    const handleInputChange = (
        e: ChangeEvent<HTMLInputElement | HTMLSelectElement>
    ) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <h2>{isLogin ? 'Login' : 'Register'}</h2>
                <div className="auth-toggle">
                    <button
                        className={isLogin ? 'active' : ''}
                        onClick={() => setIsLogin(true)}
                    >
                        Login
                    </button>
                    <button
                        className={!isLogin ? 'active' : ''}
                        onClick={() => setIsLogin(false)}
                    >
                        Register
                    </button>
                </div>

                {error && <div className="error-message">{error}</div>}

                <form onSubmit={handleSubmit}>
                    {!isLogin && (
                        <>
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
                                <label>Role</label>
                                <select
                                    name="role"
                                    value={formData.role}
                                    onChange={handleInputChange}
                                    required
                                >
                                    <option value="">Select Role</option>
                                    <option value="producer">Producer</option>
                                    <option value="distributor">Distributor</option>
                                    <option value="retailer">Retailer</option>
                                    <option value="consumer">Consumer</option>
                                </select>
                            </div>
                        </>
                    )}
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
                    {!isLogin && (
                        <div className="form-group">
                            <label>Phone</label>
                            <input
                                type="text"
                                name="phone"
                                value={formData.phone}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                    )}
                    <button type="submit">
                        {isLogin ? 'Login' : 'Register'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Auth;