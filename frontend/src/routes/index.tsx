import React from 'react';
import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import Layout from '../components/Layout';
import Login from '../pages/auth/Login';
import ConsumerProducts from '../pages/consumer/Products';
import ProducerRFID from '../pages/producer/RFID';
import StorageMonitor from '../pages/storage/Monitor';
import QCInspection from '../pages/qc/Inspection';
import NotFound from '../pages/error/NotFound';
import Orders from '../pages/consumer/Orders';
import Trace from '../pages/consumer/Trace';
import ProducerProducts from '../pages/producer/Products';
import Inventory from '../pages/storage/Inventory';
import QCReports from '../pages/qc/Reports';
import UserManagement from '../pages/admin/Users';
import SystemSettings from '../pages/admin/Settings';
import Unauthorized from '../pages/error/Unauthorized';
import RFIDQuery from '../components/RFIDQuery';
import Auth from '../pages/Auth';
import EmailVerify from '../pages/EmailVerify';
import AdminDashboard from '../pages/admin/Dashboard';
import Shop from '../pages/consumer/Shop';
import ShipmentManagement from '../pages/distributor/Shipments';
import RetailerProducts from '../pages/retailer/Products';
import ProductManagement from '../pages/producer/ProductManagement';
import ProductionManage from '../pages/admin/ProductionManage';

// 权限检查组件
interface ProtectedRouteProps {
    allowedRoles: string[];
    element: React.ReactElement;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ allowedRoles, element }) => {
    const userRole = localStorage.getItem('userRole');
    const isAuthenticated = !!localStorage.getItem('token');

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    if (!allowedRoles.includes(userRole || '')) {
        return <Navigate to="/unauthorized" replace />;
    }

    return element;
};

const AppRoutes: React.FC = () => {
    // 获取当前路径
    const currentPath = window.location.pathname;
    console.log('Current path:', currentPath);

    return (
        <Routes>
            <Route path="/auth" element={<Auth />} />
            <Route path="/verify-email" element={<EmailVerify />} />
            
            {/* 消费者路由 */}
            <Route path="/consumer" element={
                <ProtectedRoute allowedRoles={['consumer']} element={<Layout />} />
            }>
                <Route path="products" element={<ConsumerProducts />} />
                <Route path="orders" element={<Orders />} />
                <Route path="monitor" element={<StorageMonitor />} />
                <Route path="rfid" element={<RFIDQuery />} />
            </Route>

            {/* 生产商路由 */}
            <Route path="/producer" element={
                <ProtectedRoute allowedRoles={['producer']} element={<Layout />} />
            }>
                <Route path="rfid" element={<ProducerRFID />} />
                <Route path="products" element={<ProductManagement />} />
            </Route>

            {/* 仓储路由 */}
            <Route path="/storage" element={
                <ProtectedRoute allowedRoles={['storage']} element={<Layout />} />
            }>
                <Route path="monitor" element={<StorageMonitor />} />
                <Route path="inventory" element={<Inventory />} />
            </Route>

            {/* 质检路由 */}
            <Route path="/qc" element={
                <ProtectedRoute allowedRoles={['qc']} element={<Layout />} />
            }>
                <Route path="inspection" element={<QCInspection />} />
                <Route path="reports" element={<QCReports />} />
            </Route>

            {/* 管理员路由 */}
            <Route path="/admin" element={
                <ProtectedRoute allowedRoles={['admin']} element={<Layout />} />
            }>
                <Route path="dashboard" element={<AdminDashboard />} />
                <Route path="users" element={<UserManagement />} />
                <Route path="settings" element={<SystemSettings />} />
                <Route path="products" element={<RetailerProducts />} />
                <Route path="orders" element={<Orders />} />
                <Route path="shop" element={<ConsumerProducts />} />
                <Route path="monitor" element={<StorageMonitor />} />
                <Route path="rfid" element={<RFIDQuery />} />
                <Route path="inspection" element={<QCInspection />} />
                <Route path="reports" element={<QCReports />} />
                <Route path="inventory" element={<Inventory />} />
                <Route path="shipments" element={<ShipmentManagement />} />
                <Route path="production" element={<ProductionManage />} />
            </Route>

            {/* 根路径重定向 */}
            <Route path="/" element={
                (() => {
                    const token = localStorage.getItem('token');
                    if (!token) {
                        return <Navigate to="/auth" replace />;
                    }
                    const userRole = localStorage.getItem('userRole');
                    if (userRole === 'admin') {
                        return <Navigate to="/admin/dashboard" replace />;
                    }
                    return <Navigate to={`/${userRole}/products`} replace />;
                })()
            } />

            <Route path="/unauthorized" element={<Unauthorized />} />
            <Route path="*" element={<NotFound />} />
        </Routes>
    );
};

export default AppRoutes; 