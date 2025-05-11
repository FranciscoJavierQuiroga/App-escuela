// src/services/teacherService.ts
import api from './api';

export interface Teacher {
  id: number;
  user_id: number;
  hire_date: string;
  qualification: string;
  department: string;
  user?: {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
    is_active: boolean;
  };
}

export interface TeacherCreate {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  hire_date: string;
  qualification: string;
  department: string;
}

const teacherService = {
  getAll: async (): Promise<Teacher[]> => {
    const response = await api.get<Teacher[]>('/teachers/');
    return response.data;
  },
  
  getById: async (id: number): Promise<Teacher> => {
    const response = await api.get<Teacher>(`/teachers/${id}`);
    return response.data;
  },
  
  create: async (teacher: TeacherCreate): Promise<Teacher> => {
    const response = await api.post<Teacher>('/teachers/', teacher);
    return response.data;
  },
  
  update: async (id: number, teacher: Partial<Teacher>): Promise<Teacher> => {
    const response = await api.put<Teacher>(`/teachers/${id}`, teacher);
    return response.data;
  },
  
  delete: async (id: number): Promise<void> => {
    await api.delete(`/teachers/${id}`);
  }
};

export default teacherService;
