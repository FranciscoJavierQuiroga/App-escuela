// src/pages/Students/StudentFormPage.tsx
import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Grid, 
  Paper, 
  CircularProgress,
  Alert,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { format } from 'date-fns';

import studentService, { Student, StudentCreate } from '../../services/studentService';

type FormMode = 'create' | 'edit';

const initialFormState: StudentCreate = {
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  enrollment_date: format(new Date(), 'yyyy-MM-dd'),
  grade_level: 9,
  parent_name: '',
  parent_email: '',
};

const StudentFormPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [mode, setMode] = useState<FormMode>(id ? 'edit' : 'create');
  const [formData, setFormData] = useState<StudentCreate | Partial<Student>>(initialFormState);
  const [loading, setLoading] = useState(false);
  const [fetchLoading, setFetchLoading] = useState(mode === 'edit');
  const [error, setError] = useState<string | null>(null);
  const [enrollmentDate, setEnrollmentDate] = useState<Date | null>(new Date());

  useEffect(() => {
    // If editing, fetch the student data
    if (mode === 'edit' && id) {
      const fetchStudent = async () => {
        try {
          setFetchLoading(true);
          const student = await studentService.getById(parseInt(id));
          // Format data for form
          setFormData({
            first_name: student.user?.first_name || '',
            last_name: student.user?.last_name || '',
            email: student.user?.email || '',
            enrollment_date: student.enrollment_date,
            grade_level: student.grade_level,
            parent_name: student.parent_name,
            parent_email: student.parent_email,
          });
          setEnrollmentDate(new Date(student.enrollment_date));
        } catch (err: any) {
          setError('Failed to load student data: ' + (err.response?.data?.detail || err.message));
          console.error(err);
        } finally {
          setFetchLoading(false);
        }
      };

      fetchStudent();
    }
  }, [id, mode]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (e: any) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleEnrollmentDateChange = (date: Date | null) => {
    setEnrollmentDate(date);
    if (date) {
      setFormData(prev => ({ 
        ...prev, 
        enrollment_date: format(date, 'yyyy-MM-dd') 
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (mode === 'create') {
        // Ensure all required fields for student creation
        const createData = formData as StudentCreate;
        if (!createData.password) {
          throw new Error('Password is required');
        }
        
        await studentService.create(createData);
        navigate('/students');
      } else if (mode === 'edit' && id) {
        // Remove password if it's empty (don't update password)
        const updateData = { ...formData };
        if ('password' in updateData && !updateData.password) {
          delete updateData.password;
        }
        
        await studentService.update(parseInt(id), updateData);
        navigate('/students');
      }
    } catch (err: any) {
      setError('Failed to save student: ' + (err.response?.data?.detail || err.message));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (fetchLoading) {
    return <Box display="flex" justifyContent="center" mt={4}><CircularProgress /></Box>;
  }

  return (
    <Paper sx={{ p: 4, maxWidth: 800, mx: 'auto' }}>
      <Typography variant="h4" mb={4}>
        {mode === 'create' ? 'Add New Student' : 'Edit Student'}
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              fullWidth
              label="First Name"
              name="first_name"
              value={formData.first_name || ''}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              fullWidth
              label="Last Name"
              name="last_name"
              value={formData.last_name || ''}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              required
              fullWidth
              label="Email"
              name="email"
              type="email"
              value={formData.email || ''}
              onChange={handleChange}
              disabled={mode === 'edit'} // Don't allow email changes in edit mode
            />
          </Grid>
          {mode === 'create' && (
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Password"
                name="password"
                type="password"
                value={(formData as StudentCreate).password || ''}
                onChange={handleChange}
              />
            </Grid>
          )}
          {mode === 'edit' && (
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="New Password (leave blank to keep current)"
                name="password"
                type="password"
                value={(formData as any).password || ''}
                onChange={handleChange}
              />
            </Grid>
          )}
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel id="grade-level-label">Grade Level</InputLabel>
              <Select
                labelId="grade-level-label"
                name="grade_level"
                value={formData.grade_level || 9}
                label="Grade Level"
                onChange={handleSelectChange}
              >
                {[7, 8, 9, 10, 11, 12].map((grade) => (
                  <MenuItem key={grade} value={grade}>
                    Grade {grade}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DatePicker
                label="Enrollment Date"
                value={enrollmentDate}
                onChange={handleEnrollmentDateChange}
                format="yyyy-MM-dd"
              />
            </LocalizationProvider>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              fullWidth
              label="Parent Name"
              name="parent_name"
              value={formData.parent_name || ''}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              fullWidth
              label="Parent Email"
              name="parent_email"
              type="email"
              value={formData.parent_email || ''}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sx={{ mt: 2 }}>
            <Box display="flex" justifyContent="space-between">
              <Button
                variant="outlined"
                onClick={() => navigate('/students')}
                disabled={loading}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : (mode === 'create' ? 'Create Student' : 'Update Student')}
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Box>
    </Paper>
  );
};

export default StudentFormPage;
