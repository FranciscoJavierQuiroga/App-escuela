// src/components/Layout/Layout.tsx
import React, { ReactNode } from 'react';
import { Container, Box, CssBaseline } from '@mui/material';
import Navbar from './Navbar';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <CssBaseline />
      <Navbar />
      <Container component="main" sx={{ flexGrow: 1, py: 4 }}>
        {children}
      </Container>
      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          backgroundColor: (theme) => theme.palette.grey[200],
        }}
      >
        <Container maxWidth="sm">
          <Box textAlign="center">
            <Box component="p" sx={{ mb: 0 }}>
              © {new Date().getFullYear()} School Management System
            </Box>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default Layout;
