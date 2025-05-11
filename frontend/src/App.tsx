// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';

// Context
import { AuthProvider } from './context/AuthContext';

// Components
import Layout from './components/Layout/Layout';
import PrivateRoute from './components/PrivateRoute';

// Pages
import LoginPage from './pages/Login/LoginPage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import StudentListPage from './pages/Students/StudentListPage';
import StudentFormPage from './pages/Students/StudentFormPage';
import StudentDetailPage from './pages/Students/StudentDetailPage';
import MyGradesPage from './pages/Students/MyGradesPage';
import UnauthorizedPage from './pages/Error/UnauthorizedPage';
import ProfilePage from './pages/Profile/ProfilePage';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: [
      'Roboto',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Layout>
            <Routes>
              {/* Public routes */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/unauthorized" element={<UnauthorizedPage />} />
              
              {/* Private routes */}
              <Route 
                path="/" 
                element={
                  <PrivateRoute>
                    <DashboardPage />
                  </PrivateRoute>
                } 
              />

              {/* Profile - accessible to all logged in users */}
              <Route 
                path="/profile" 
                element={
                  <PrivateRoute>
                    <ProfilePage />
                  </PrivateRoute>
                } 
              />
              
              {/* Student routes - Admin only */}
              <Route 
                path="/students" 
                element={
                  <PrivateRoute roles={['ADMIN', 'TEACHER']}>
                    <StudentListPage />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/students/new" 
                element={
                  <PrivateRoute roles={['ADMIN']}>
                    <StudentFormPage />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/students/:id" 
                element={
                  <PrivateRoute roles={['ADMIN', 'TEACHER']}>
                    <StudentDetailPage />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/students/:id/edit" 
                element={
                  <PrivateRoute roles={['ADMIN']}>
                    <StudentFormPage />
                  </PrivateRoute>
                } 
              />
              
              {/* Student view of their own grades */}
              <Route 
                path="/my-grades" 
                element={
                  <PrivateRoute roles={['STUDENT']}>
                    <MyGradesPage />
                  </PrivateRoute>
                } 
              />
              
              {/* Catch all route */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Layout>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
