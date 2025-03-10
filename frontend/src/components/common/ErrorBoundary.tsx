import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
    children: ReactNode;
}

interface State {
    hasError: boolean;
    error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false
    };

    public static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Uncaught error:', error, errorInfo);
    }

    public render() {
        if (this.state.hasError) {
            return (
                <div className="container mt-5">
                    <div className="alert alert-danger">
                        <h4 className="alert-heading">
                            System Error
                            <small className="d-block text-muted">系统错误</small>
                        </h4>
                        <p>
                            An unexpected error occurred. Please try again later.
                            <small className="d-block text-muted">发生意外错误，请稍后重试。</small>
                        </p>
                        <button 
                            className="btn btn-outline-danger"
                            onClick={() => this.setState({ hasError: false })}
                        >
                            Retry
                            <small className="d-block">重试</small>
                        </button>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary; 