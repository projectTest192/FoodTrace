import React from 'react';
import { useNavigate } from 'react-router-dom';

const Unauthorized: React.FC = () => {
    const navigate = useNavigate();

    return (
        <div className="container mt-5">
            <div className="text-center">
                <h1>401 Unauthorized未授权</h1>
                <p className="lead">
                    You don't have permission to access this page.
                    <br />
                    您没有权限访问此页面。
                </p>
                <button 
                    className="btn btn-primary"
                    onClick={() => navigate(-1)}
                >
                    Go Back返回
                </button>
            </div>
        </div>
    );
};

export default Unauthorized; 