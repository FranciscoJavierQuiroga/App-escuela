// src/pages/Students/MyGradesPage.tsx
import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  CircularProgress,
  Paper,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  Button,
  useTheme
} from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';

import studentService from '../../services/studentService';
import { useAuth } from '../../context/AuthContext';
import { formatDate, downloadFile, createTimestampedFilename } from '../../utils/fileUtils';

const MyGradesPage: React.FC = () => {
  const { user } = useAuth();
  const theme = useTheme();
  const [studentId, setStudentId] = useState<number | null>(null);
  const [grades, setGrades] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // First get student ID from current user
  useEffect(() => {
    const findStudentId = async () => {
      if (!user) return;
      
      try {
        const students = await studentService.getAll();
        const myStudentProfile = students.find(s => s.user_id === user.id);
        
        if (myStudentProfile) {
          setStudentId(myStudentProfile.id);
        } else {
          setError('Could not find your student profile');
        }
      } catch (err: any) {
        setError('Failed to load your student information: ' + (err.response?.data?.detail || err.message));
        console.error(err);
      }
    };

    findStudentId();
  }, [user]);

  // Then get grades using student ID
  useEffect(() => {
    const fetchGrades = async () => {
      if (!studentId) return;
      
      try {
        setLoading(true);
        const gradesData = await studentService.getStudentGrades(studentId);
        setGrades(gradesData);
      } catch (err: any) {
        setError('Failed to load your grades: ' + (err.response?.data?.detail || err.message));
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (studentId) {
      fetchGrades();
    }
  }, [studentId]);

  const handleDownloadTranscript = async () => {
    if (!studentId) return;
    
    try {
      const blobData = await studentService.downloadTranscript(studentId);
      const filename = createTimestampedFilename('my_transcript', 'pdf');
      downloadFile(blobData, filename, 'application/pdf');
    } catch (err: any) {
      setError('Failed to download transcript: ' + (err.response?.data?.detail || err.message));
      console.error(err);
    }
  };

  if (loading) {
    return <Box display="flex" justifyContent="center" mt={4}><CircularProgress /></Box>;
  }

  // Calculate GPA if grades available
  let gpa = 0;
  let gradedCourses = 0;
  if (grades?.grades) {
    grades.grades.forEach((grade: any) => {
      if (grade.grade !== null) {
        gpa += grade.grade;
        gradedCourses++;
      }
    });
    
    if (gradedCourses > 0) {
      gpa = gpa / gradedCourses;
    }
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">My Grades</Typography>
        
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={<DownloadIcon />}
          onClick={handleDownloadTranscript}
        >
          Download Transcript
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardHeader title="Academic Summary" />
            <Divider />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <Paper 
                    elevation={3} 
                    sx={{ 
                      p: 3, 
                      textAlign: 'center',
                      backgroundColor: theme.palette.primary.light,
                      color: theme.palette.primary.contrastText
                    }}
                  >
                    <Typography variant="h6" gutterBottom>
                      Average Grade (GPA)
                    </Typography>
                    <Typography variant="h3">
                      {gradedCourses > 0 ? gpa.toFixed(2) : 'N/A'}
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Paper 
                    elevation={3} 
                    sx={{ 
                      p: 3, 
                      textAlign: 'center',
                      backgroundColor: theme.palette.secondary.light,
                      color: theme.palette.secondary.contrastText
                    }}
                  >
                    <Typography variant="h6" gutterBottom>
                      Enrolled Courses
                    </Typography>
                    <Typography variant="h3">
                      {grades?.grades?.length || 0}
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Paper 
                    elevation={3} 
                    sx={{ 
                      p: 3, 
                      textAlign: 'center',
                      backgroundColor: theme.palette.info.light,
                      color: theme.palette.info.contrastText
                    }}
                  >
                    <Typography variant="h6" gutterBottom>
                      Graded Courses
                    </Typography>
                    <Typography variant="h3">
                      {gradedCourses} / {grades?.grades?.length || 0}
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardHeader title="My Course Grades" />
            <Divider />
            <CardContent>
              {grades?.grades && grades.grades.length > 0 ? (
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Course Code</TableCell>
                        <TableCell>Course Name</TableCell>
                        <TableCell>Enrollment Date</TableCell>
                        <TableCell align="right">Grade</TableCell>
                        <TableCell>Grade Date</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {grades.grades.map((grade: any) => (
                        <TableRow key={grade.course_id}>
                          <TableCell>{grade.course_code}</TableCell>
                          <TableCell>{grade.course_name}</TableCell>
                          <TableCell>{formatDate(grade.enrollment_date)}</TableCell>
                          <TableCell 
                            align="right"
                            sx={{
                              color: grade.grade !== null ? (
                                grade.grade >= 90 ? 'success.main' :
                                grade.grade >= 80 ? 'success.main' :
                                grade.grade >= 70 ? 'primary.main' :
                                grade.grade >= 60 ? 'warning.main' : 'error.main'
                              ) : 'text.secondary'
                            }}
                          >
                            <Typography fontWeight="bold">
                              {grade.grade !== null ? grade.grade : 'Not graded'}
                            </Typography>
                          </TableCell>
                          <TableCell>{grade.grade_date ? formatDate(grade.grade_date) : 'N/A'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Typography align="center">
                  You are not enrolled in any courses yet.
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default MyGradesPage;
