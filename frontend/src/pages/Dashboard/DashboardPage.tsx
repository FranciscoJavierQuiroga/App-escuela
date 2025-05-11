// src/pages/Dashboard/DashboardPage.tsx
import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  Paper, 
  CircularProgress,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Button
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import studentService from '../../services/studentService';
import teacherService from '../../services/teacherService';
import courseService from '../../services/courseService';

// Dashboard statistics interface
interface DashboardStats {
  students: number;
  teachers: number;
  courses: number;
}

const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState<DashboardStats>({ students: 0, teachers: 0, courses: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [studentInfo, setStudentInfo] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Load stats based on user role
        if (user?.role === 'ADMIN' || user?.role === 'TEACHER') {
          // For admin and teachers, load overall stats
          const studentsData = await studentService.getAll();
          const teachersData = await teacherService.getAll();
          const coursesData = await courseService.getAll();
          
          setStats({
            students: studentsData.length,
            teachers: teachersData.length,
            courses: coursesData.length,
          });
        } else if (user?.role === 'STUDENT') {
          // For students, load their specific data
          // Find the student ID from the user info
          const students = await studentService.getAll();
          const currentStudent = students.find(s => s.user_id === user.id);
          
          if (currentStudent) {
            const grades = await studentService.getStudentGrades(currentStudent.id);
            setStudentInfo({
              student: currentStudent,
              grades: grades
            });
          }
          
          // Still get basic stats
          const coursesData = await courseService.getAll();
          setStats({
            students: students.length,
            teachers: 0, // Don't need to fetch teachers for student view
            courses: coursesData.length,
          });
        }
      } catch (err: any) {
        setError('Failed to load dashboard data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [user]);
  
  if (loading) {
    return <Box display="flex" justifyContent="center" mt={4}><CircularProgress /></Box>;
  }
  
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      {error && (
        <Paper sx={{ p: 2, mb: 2, bgcolor: 'error.light' }}>
          <Typography color="error">{error}</Typography>
        </Paper>
      )}
      
      <Typography variant="h6" gutterBottom>
        Welcome, {user?.first_name || 'User'}!
      </Typography>
      
      <Grid container spacing={3} sx={{ mt: 1 }}>
        {/* Show different cards based on user role */}
        {(user?.role === 'ADMIN' || user?.role === 'TEACHER') && (
          <>
            <Grid item xs={12} sm={4}>
              <Card>
                <CardHeader title="Students" />
                <Divider />
                <CardContent>
                  <Typography variant="h3" align="center">{stats.students}</Typography>
                  <Box display="flex" justifyContent="center" mt={2}>
                    <Button 
                      variant="contained" 
                      onClick={() => navigate('/students')}
                    >
                      View Students
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} sm={4}>
              <Card>
                <CardHeader title="Teachers" />
                <Divider />
                <CardContent>
                  <Typography variant="h3" align="center">{stats.teachers}</Typography>
                  <Box display="flex" justifyContent="center" mt={2}>
                    <Button 
                      variant="contained" 
                      onClick={() => navigate('/teachers')}
                    >
                      View Teachers
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} sm={4}>
              <Card>
                <CardHeader title="Courses" />
                <Divider />
                <CardContent>
                  <Typography variant="h3" align="center">{stats.courses}</Typography>
                  <Box display="flex" justifyContent="center" mt={2}>
                    <Button 
                      variant="contained" 
                      onClick={() => navigate('/courses')}
                    >
                      View Courses
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </>
        )}
        
        {/* Student specific view */}
        {user?.role === 'STUDENT' && studentInfo && (
          <>
            <Grid item xs={12} sm={6}>
              <Card>
                <CardHeader title="My Information" />
                <Divider />
                <CardContent>
                  <Typography><strong>Grade Level:</strong> {studentInfo.student.grade_level}</Typography>
                  <Typography><strong>Enrollment Date:</strong> {new Date(studentInfo.student.enrollment_date).toLocaleDateString()}</Typography>
                  <Box display="flex" justifyContent="center" mt={2}>
                    <Button 
                      variant="contained" 
                      onClick={() => navigate('/my-grades')}
                    >
                      View My Grades
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Card>
                <CardHeader title="My Courses" />
                <Divider />
                <CardContent>
                  {studentInfo.grades.grades && studentInfo.grades.grades.length > 0 ? (
                    <>
                      <Typography variant="h6" align="center">{studentInfo.grades.grades.length} Enrolled Courses</Typography>
                      <Box sx={{ mt: 2 }}>
                        {studentInfo.grades.grades.slice(0, 3).map((grade: any) => (
                          <Box key={grade.course_id} sx={{ mb: 1 }}>
                            <Typography>{grade.course_name}</Typography>
                            <Typography variant="body2" color="textSecondary">
                              Grade: {grade.grade !== null ? grade.grade : 'Not graded yet'}
                            </Typography>
                            <Divider sx={{ mt: 1 }} />
                          </Box>
                        ))}
                        {studentInfo.grades.grades.length > 3 && (
                          <Box display="flex" justifyContent="center" mt={1}>
                            <Button size="small" onClick={() => navigate('/my-grades')}>
                              View all courses
                            </Button>
                          </Box>
                        )}
                      </Box>
                    </>
                  ) : (
                    <Typography align="center">You are not enrolled in any courses yet.</Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </>
        )}
        
        {/* Quick Actions Card */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="Quick Actions" />
            <Divider />
            <CardContent>
              <Grid container spacing={2}>
                {user?.role === 'ADMIN' && (
                  <>
                    <Grid item xs={12} sm={4}>
                      <Button fullWidth variant="outlined" onClick={() => navigate('/students/new')}>
                        Add New Student
                      </Button>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <Button fullWidth variant="outlined" onClick={() => navigate('/teachers/new')}>
                        Add New Teacher
                      </Button>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <Button fullWidth variant="outlined" onClick={() => navigate('/courses/new')}>
                        Create New Course
                      </Button>
                    </Grid>
                  </>
                )}
                
                {user?.role === 'TEACHER' && (
                  <>
                    <Grid item xs={12} sm={6}>
                      <Button fullWidth variant="outlined" onClick={() => navigate('/courses/new')}>
                        Create New Course
                      </Button>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <Button fullWidth variant="outlined" onClick={() => navigate('/grades')}>
                        Manage Grades
                      </Button>
                    </Grid>
                  </>
                )}
                
                {user?.role === 'STUDENT' && (
                  <>
                    <Grid item xs={12} sm={6}>
                      <Button 
                        fullWidth 
                        variant="outlined" 
                        onClick={() => navigate('/courses')}
                      >
                        Browse Courses
                      </Button>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <Button 
                        fullWidth 
                        variant="outlined" 
                        onClick={() => {
                          if (studentInfo?.student?.id) {
                            // Open the PDF in a new tab
                            window.open(`/reports/students/${studentInfo.student.id}/transcript`, '_blank');
                          }
                        }}
                      >
                        Download Transcript
                      </Button>
                    </Grid>
                  </>
                )}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage;
