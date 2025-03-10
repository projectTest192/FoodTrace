import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import EmailVerify from './pages/EmailVerify';
import ProtectedRoute from './components/ProtectedRoute';

// Admin pages
import AdminDashboard from './pages/admin/Dashboard';
import UserManagement from './pages/admin/Users';

// Producer pages
import ProducerProducts from './pages/producer/Products';
import ProductManagement from './pages/producer/ProductManagement';
import RFID from './pages/producer/RFID';

// Distributor pages
import Shipments from './pages/distributor/Shipments';

// Retailer pages
import RetailerProducts from './pages/retailer/Products';

// Consumer pages
import ConsumerProducts from './pages/consumer/Products';
import ConsumerOrders from './pages/consumer/Orders';
import Trace from './pages/consumer/Trace';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* Public Routes */}
                <Route path="/auth" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/verify-email" element={<EmailVerify />} />

                {/* Protected Routes */}
                <Route path="/admin" element={
                    <ProtectedRoute allowedRoles={['admin']}>
                        <Layout />
                    </ProtectedRoute>
                }>
                    <Route path="dashboard" element={<AdminDashboard />} />
                    <Route path="users" element={<UserManagement />} />
                </Route>

                <Route path="/producer" element={
                    <ProtectedRoute allowedRoles={['producer']}>
                        <Layout />
                    </ProtectedRoute>
                }>
                    <Route path="products" element={<ProducerProducts />} />
                    <Route path="management" element={<ProductManagement />} />
                    <Route path="rfid" element={<RFID />} />
                </Route>

                <Route path="/distributor" element={
                    <ProtectedRoute allowedRoles={['distributor']}>
                        <Layout />
                    </ProtectedRoute>
                }>
                    <Route path="shipments" element={<Shipments />} />
                </Route>

                <Route path="/retailer" element={
                    <ProtectedRoute allowedRoles={['retailer']}>
                        <Layout />
                    </ProtectedRoute>
                }>
                    <Route path="products" element={<RetailerProducts />} />
                </Route>

                <Route path="/consumer" element={
                    <ProtectedRoute allowedRoles={['consumer']}>
                        <Layout />
                    </ProtectedRoute>
                }>
                    <Route path="products" element={<ConsumerProducts />} />
                    <Route path="orders" element={<ConsumerOrders />} />
                    <Route path="trace" element={<Trace />} />
                </Route>

                {/* Default Route */}
                <Route path="/" element={<Navigate to="/auth" replace />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App; 