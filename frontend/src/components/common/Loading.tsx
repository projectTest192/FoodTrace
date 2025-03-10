import React from 'react';

interface LoadingProps {
    text?: string;
    textCn?: string;
}

const Loading: React.FC<LoadingProps> = ({ 
    text = 'Loading', 
    textCn = '加载中' 
}) => {
    return (
        <div className="d-flex flex-column align-items-center justify-content-center" style={{ minHeight: '200px' }}>
            <div className="spinner-border text-primary mb-2" role="status">
                <span className="visually-hidden">Loading...</span>
            </div>
            <div>
                {text}
                <small className="d-block text-muted">{textCn}</small>
            </div>
        </div>
    );
};

export default Loading; 