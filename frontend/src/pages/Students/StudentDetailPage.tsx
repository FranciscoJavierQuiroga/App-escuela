// src/pages/Students/StudentDetailPage.tsx
import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
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
  IconButton,
  Tooltip
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import EditIcon from '@mui/icons-material/Edit';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import DownloadIcon from '@mui/icons-material/Download';

import studentService, { Student } from '../../services/studentService';
import { formatDate, downloadFile, createTimestampedFilename } from '../../utils/fileUtils';

const StudentDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [student, setStudent] = useState<Student | null>(null);
  const [grades, setGrades] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStudentAndGrades = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        const studentId = parseInt(id);
        
        // Fetch student details
        const studentData = await studentService.getById(studentId);
        setStudent(studentData);
        
        // Fetch student grades
        const gradesData = await studentService.getStudentGrades(studentId);
        setGrades(gradesData);
      } catch (err: any) {
        setError('Failed to load student data: ' + (err.response?.data?.detail || err.message));
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchStudentAndGrades();
  }, [id]);

  const handleDownloadTranscript = async () => {
    if (!id) return;
    
    try {
      const blobData = await studentService.downloadTranscript(parseInt(id));
      const filename = createTimestampedFilename('transcript_student_' + id, 'pdf');
      downloadFile(blobData, filename, 'application/pdf');
    } catch (err: any) {
      setError('Failed to download transcript: ' + (err.response?.data?.detail || err.message));
      console.error(err);
    }
  };

  if (loading) {
    return <Box display="flex" justifyContent="center" mt={4}><CircularProgress /></Box>;
  }

  if (!student) {
    return (
      <Alert severity="error">
        Student not found
      </Alert>
    );
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
        <Box display="flex" alignItems="center">
          <IconButton onClick={() => navigate('/students')} sx={{ mr: 1 }}>
            <ArrowBackIcon />
          </IconButton>
          <Typography variant="h4">Student Details</Typography>
        </Box>
        <Box>
          <Tooltip title="Download Transcript">
            <IconButton 
              color="primary"
              onClick={handleDownloadTranscript}
              sx={{ mr: 1 }}
            >
              <DownloadIcon />
            </IconButton>
          </Tooltip>
          <Button 
            variant="contained" 
            color="primary" 
            startIcon={<EditIcon />}
            onClick={() => navigate(`/students/${id}/edit`)}
          >
            Edit Student
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Personal Information" />
            <Divider />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1" color="textSecondary">
                    Full Name
                  </Typography>
                  <Typography variant="body1">
                    {student.user?.first_name} {student.user?.last_name}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1" color="textSecondary">
                    Email
                  </Typography>
                  <Typography variant="body1">
                    {student.user?.email}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1" color="textSecondary">
                    Grade Level
                  </Typography>
                  <Typography variant="body1">
                    Grade {student.grade_level}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1" color="textSecondary">
                    Enrollment Date
                  </Typography>
                  <Typography variant="body1">
                    {formatDate(student.enrollment_date)}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1" color="textSecondary">
                    Parent Name
                  </Typography>
                  <Typography variant="body1">
                    {student.parent_name}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1" color="textSecondary">
                    Parent Email
                  </Typography>
                  <Typography variant="body1">
                    {student.parent_email}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader 
              title="Academic Summary" 
              action={
                <Button 
                  size="small" 
                  variant="outlined"
                  onClick={handleDownloadTranscript}
                >
                  Download Transcript
                </Button>
              }
            />
            <Divider />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1" color="textSecondary">
                    GPA
                  </Typography>
                  <Typography variant="h4">
                    {gradedCourses > 0 ? gpa.toFixed(2) : 'N/A'}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1" color="textSecondary">
                    Enrolled Courses
                  </Typography>
                  <Typography variant="h4">
                    {grades?.grades?.length || 0}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardHeader title="Course Grades" />
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
                          <TableCell align="right">{grade.grade !== null ? grade.grade : 'Not graded'}</TableCell>
                          <TableCell>{grade.grade_date ? formatDate(grade.grade_date) : 'N/A'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Typography align="center">
                  No courses or grades found for this student.
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StudentDetailPage;
