import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { verifyEmail } from '../api/auth';
import '../styles/email-verify.css';  // 创建新的样式文件

const EmailVerify: React.FC = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const [status, setStatus] = useState<'verifying' | 'success' | 'error'>('verifying');
    const [message, setMessage] = useState('Verifying email...');  // 修改为英文

    useEffect(() => {
        const verifyToken = async () => {
            try {
                const token = searchParams.get('token');
                if (!token) {
                    setStatus('error');
                    setMessage('Invalid verification link');  // 修改为英文
                    return;
                }

                await verifyEmail(token);
                setStatus('success');
                setMessage('Email verified successfully!');  // 修改为英文
                
                // 3秒后自动跳转到登录页
                setTimeout(() => {
                    navigate('/auth');
                }, 3000);
            } catch (error) {
                setStatus('error');
                setMessage('Verification failed. Please try again or contact administrator');  // 修改为英文
            }
        };

        verifyToken();
    }, [searchParams, navigate]);

    return (
        <div className="email-verify-container">
            <div className="email-verify-card">
                <div className="verify-status-icon">
                    {status === 'verifying' && <div className="spinner"></div>}
                    {status === 'success' && <div className="success-icon">✓</div>}
                    {status === 'error' && <div className="error-icon">✗</div>}
                </div>

                <h2 className={`verify-message ${status}`}>{message}</h2>
                
                {(status === 'success' || status === 'error') && (
                    <div className="verify-actions">
                        <p className="redirect-message">
                            {status === 'success' ? 'Redirecting to login page in 3 seconds...' : ''}  {/* 修改为英文 */}
                        </p>
                        <button
                            className="login-button"
                            onClick={() => navigate('/auth')}
                        >
                            Go to Login  {/* 修改为英文 */}
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default EmailVerify; 