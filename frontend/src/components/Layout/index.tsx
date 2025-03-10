import React from 'react';
import { Outlet, Navigate, useNavigate } from 'react-router-dom';
import { Layout as AntLayout, Button } from 'antd';
import { LogoutOutlined, UserOutlined } from '@ant-design/icons';
import Sidebar from './Sidebar';
import './Layout.css';

const { Content, Sider } = AntLayout;

// 辅助函数：格式化角色名称
const formatRole = (role: string | null): string => {
    if (!role) return 'User';
    return role.charAt(0).toUpperCase() + role.slice(1).toLowerCase();
};

// 辅助函数：获取角色显示名称
const getRoleDisplay = (role: string | null): string => {
    if (!role) return 'User';
    const roleMap: { [key: string]: string } = {
        consumer: 'Consumer',
        producer: 'Producer',
        distributor: 'Distributor',
        retailer: 'Retailer',
        admin: 'Administrator'
    };
    return roleMap[role.toLowerCase()] || formatRole(role);
};

const Layout: React.FC = () => {
    const navigate = useNavigate();
    const token = localStorage.getItem('token');
    if (!token) {
        return <Navigate to="/login" replace />;
    }

    const userEmail = localStorage.getItem('userEmail');
    const userRole = localStorage.getItem('userRole');

    const handleLogout = () => {
        localStorage.clear();
        navigate('/auth');
    };

    return (
        <AntLayout style={{ minHeight: '100vh' }}>
            <Sider width={250}>
                <div className="logo-container">
                    <h3>Food Trace System</h3>
                    <div className="user-info">
                        <div className="user-role">
                            <UserOutlined style={{ marginRight: 8 }} />
                            {userRole}
                        </div>
                        <div className="user-email">{userEmail}</div>
                        <Button 
                            type="text" 
                            danger
                            icon={<LogoutOutlined />}
                            onClick={handleLogout}
                            className="logout-button"
                        >
                            Logout
                        </Button>
                    </div>
                </div>
                <Sidebar />
            </Sider>
            <AntLayout>
                <Content style={{ margin: '24px 16px', padding: 24, background: '#fff' }}>
                    <Outlet />
                </Content>
            </AntLayout>
        </AntLayout>
    );
};

export default Layout; 