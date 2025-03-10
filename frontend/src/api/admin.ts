import api from './axios';

interface EnterpriseUser {
    name: string;
    email: string;
    pwd: string;
    role: string;
    phone?: string;
}

export const createEnterpriseUser = async (userData: EnterpriseUser): Promise<void> => {
    await api.post('/admin/users/enterprise', userData);
};

export const getUsersByRole = async (role: string) => {
    const response = await api.get(`/admin/users/${role}`);
    return response.data;
}; 