// src/services/studentService.ts
import api from './api';

export interface Student {
  id: number;
  user_id: number;
  enrollment_date: string;
  grade_level: number;
  parent_name: string;
  parent_email: string;
  user?: {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
    is_active: boolean;
  };
}

export interface StudentCreate {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  enrollment_date: string;
  grade_level: number;
  parent_name: string;
  parent_email: string;
}

const studentService = {
  getAll: async (): Promise<Student[]> => {
    const response = await api.get<Student[]>('/students/');
    return response.data;
  },
  
  getById: async (id: number): Promise<Student> => {
    const response = await api.get<Student>(`/students/${id}`);
    return response.data;
  },
  
  create: async (student: StudentCreate): Promise<Student> => {
    const response = await api.post<Student>('/students/', student);
    return response.data;
  },
  
  update: async (id: number, student: Partial<Student>): Promise<Student> => {
    const response = await api.put<Student>(`/students/${id}`, student);
    return response.data;
  },
  
  delete: async (id: number): Promise<void> => {
    await api.delete(`/students/${id}`);
  },
  
  getStudentGrades: async (id: number): Promise<any> => {
    const response = await api.get(`/reports/students/${id}/grades`);
    return response.data;
  },
  
  downloadTranscript: async (id: number): Promise<Blob> => {
    const response = await api.get(`/reports/students/${id}/transcript`, {
      responseType: 'blob'
    });
    return response.data;
  }
};

export default studentService;
