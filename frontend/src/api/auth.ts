import axios from 'axios';

interface UserLogin {
    email: string;
    pwd: string;
}

interface UserRegister extends UserLogin {
    userEmail: string;
    userRole: string;
}

interface LoginResponse {
    accToken: string;
    tokenType: string;
    user: {
        id: number;
        name: string;
        email: string;
        role: string;
        active: boolean;
        verified: boolean;
    };
}

interface RegisterData {
    name: string;
    email: string;
    pwd: string;
    phone?: string;
}

interface ApiError {
    type: string;
    loc: string[];
    msg: string;
    input: string;
}

export const login = async (userData: UserLogin): Promise<LoginResponse> => {
    try {
        const response = await axios.post<LoginResponse>(
            'http://localhost:8002/api/auth/login', 
            {
                email: userData.email,
                pwd: userData.pwd
            }
        );
        return response.data;
    } catch (error: any) {
        console.error('Login error:', error.response?.data || error);
        throw error;
    }
};

export const register = async (data: RegisterData) => {
    try {
        const response = await axios.post('http://localhost:8002/api/auth/register/consumer', {
            name: data.name,
            email: data.email,
            pwd: data.pwd,
            phone: data.phone
        });
        return response.data;
    } catch (error: any) {
        if (error.response?.data) {
            if (Array.isArray(error.response.data)) {
                throw new Error(error.response.data.map((err: any) => err.msg).join(', '));
            }
            if (error.response.data.detail) {
                throw new Error(error.response.data.detail);
            }
        }
        throw new Error('注册失败，请重试');
    }
};

export const verifyEmail = async (token: string): Promise<void> => {
    await axios.get(`http://localhost:8002/api/auth/verify-email?token=${token}`);
};