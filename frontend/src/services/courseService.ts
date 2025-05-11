// src/services/courseService.ts
import api from './api';

export interface Course {
  id: number;
  name: string;
  code: string;
  description: string;
  credits: number;
  teacher_id?: number;
  teacher?: {
    id: number;
    user_id: number;
    user?: {
      first_name: string;
      last_name: string;
    };
  };
}

export interface CourseCreate {
  name: string;
  code: string;
  description: string;
  credits: number;
  teacher_id?: number;
}

const courseService = {
  getAll: async (): Promise<Course[]> => {
    const response = await api.get<Course[]>('/courses/');
    return response.data;
  },
  
  getById: async (id: number): Promise<Course> => {
    const response = await api.get<Course>(`/courses/${id}`);
    return response.data;
  },
  
  create: async (course: CourseCreate): Promise<Course> => {
    const response = await api.post<Course>('/courses/', course);
    return response.data;
  },
  
  update: async (id: number, course: Partial<Course>): Promise<Course> => {
    const response = await api.put<Course>(`/courses/${id}`, course);
    return response.data;
  },
  
  delete: async (id: number): Promise<void> => {
    await api.delete(`/courses/${id}`);
  },
  
  getEnrolledStudents: async (courseId: number): Promise<any[]> => {
    const response = await api.get(`/courses/${courseId}/students`);
    return response.data;
  }
};

export default courseService;
