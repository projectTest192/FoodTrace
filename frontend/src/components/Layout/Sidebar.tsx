import React from 'react';
import { Menu } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import {
    DashboardOutlined,
    UserOutlined,
    SettingOutlined,
    ShoppingCartOutlined,
    OrderedListOutlined,
    MonitorOutlined,
    ScanOutlined,
    CarOutlined,
    ClockCircleOutlined,
    SearchOutlined,
    BoxPlotOutlined,
    EnvironmentOutlined,
    DatabaseOutlined
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

type MenuItem = Required<MenuProps>['items'][number];

const Sidebar: React.FC = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const userRole = localStorage.getItem('userRole');

    // 定义不同角色的导航菜单
    const menuItems: { [key: string]: MenuItem[] } = {
        // 消费者菜单
        consumer: [
            {
                key: '/consumer/products',
                icon: <ShoppingCartOutlined />,
                label: 'Product Purchase'
            },
            {
                key: '/consumer/orders',
                icon: <ClockCircleOutlined />,
                label: 'Order History'
            },
            {
                key: '/consumer/trace',
                icon: <SearchOutlined />,
                label: 'Product Tracing'
            }
        ],
        
        // 生产商菜单
        producer: [
            {
                key: '/producer/products',
                icon: <BoxPlotOutlined />,
                label: 'Product Management'
            },
            {
                key: '/producer/rfid',
                icon: <ScanOutlined />,
                label: 'RFID Management'
            }
        ],
        
        // 配送商菜单
        distributor: [
            {
                key: '/distributor/shipments',
                icon: <CarOutlined />,
                label: 'Shipment Management'
            },
            {
                key: '/distributor/monitor',
                icon: <MonitorOutlined />,
                label: 'Transport Monitor'
            }
        ],
        
        // 零售商菜单
        retailer: [
            {
                key: '/retailer/products',
                icon: <BoxPlotOutlined />,
                label: 'Product Management'
            },
            {
                key: '/retailer/orders',
                icon: <OrderedListOutlined />,
                label: 'Order Management'
            }
        ],
        
        // 管理员菜单
        admin: [
            {
                key: '/admin/dashboard',
                icon: <DashboardOutlined />,
                label: 'Dashboard'
            },
            {
                key: '/admin/users',
                icon: <UserOutlined />,
                label: 'User Management'
            },
            {
                key: '/admin/settings',
                icon: <SettingOutlined />,
                label: 'System Settings'
            },
            {
                key: '/admin/products',
                icon: <ShoppingCartOutlined />,
                label: 'Product Management'
            },
            {
                key: '/admin/orders',
                icon: <OrderedListOutlined />,
                label: 'Order Management'
            },
            {
                key: '/admin/shop',
                icon: <ShoppingCartOutlined />,
                label: 'Product Purchase'
            },
            {
                key: '/admin/monitor',
                icon: <MonitorOutlined />,
                label: 'Transport Monitor'
            },
            {
                key: '/admin/rfid',
                icon: <ScanOutlined />,
                label: 'RFID Management'
            },
            {
                key: '/admin/shipments',
                icon: <CarOutlined />,
                label: 'Shipment Management'
            },
            {
                key: '/admin/production',
                icon: <BoxPlotOutlined />,
                label: 'Production Management'
            }
        ]
    };

    const handleMenuClick = (key: string) => {
        navigate(key);
    };

    return (
        <Menu
            mode="inline"
            selectedKeys={[location.pathname]}
            style={{ borderRight: 0 }}
            items={menuItems[userRole as keyof typeof menuItems] || []}
            onClick={({ key }) => handleMenuClick(key as string)}
        />
    );
};

export default Sidebar; 