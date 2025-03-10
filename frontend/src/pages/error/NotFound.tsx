import React from 'react';
import { Link } from 'react-router-dom';

const NotFound: React.FC = () => {
    return (
        <div className="container mt-5 text-center">
            <h1 className="display-1">404</h1>
            <h2>
                Page Not Found
                <small className="d-block text-muted">页面未找到</small>
            </h2>
            <p className="lead">
                The page you are looking for does not exist.
                <small className="d-block text-muted">您访问的页面不存在。</small>
            </p>
            <Link to="/" className="btn btn-primary">
                Back to Home
                <small className="d-block">返回首页</small>
            </Link>
        </div>
    );
};

export default NotFound; 