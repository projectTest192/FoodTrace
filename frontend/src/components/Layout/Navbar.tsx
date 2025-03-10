import React from 'react';
import { useNavigate } from 'react-router-dom';

const Navbar: React.FC = () => {
    const navigate = useNavigate();
    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-light">
            <div className="container-fluid">
                <button 
                    className="btn btn-outline-secondary"
                    onClick={handleLogout}
                >
                    Logout退出
                </button>
            </div>
        </nav>
    );
};

export default Navbar; 