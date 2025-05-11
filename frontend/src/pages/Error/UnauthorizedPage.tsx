// src/pages/Error/UnauthorizedPage.tsx
import React from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Paper,
  Container
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const UnauthorizedPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 4, textAlign: 'center' }}>
        <Typography variant="h4" color="error" gutterBottom>
          Access Denied
        </Typography>
        
        <Typography variant="body1" paragraph>
          You don't have permission to access this page.
        </Typography>
        
        <Typography variant="body2" color="textSecondary" paragraph>
          Your current role is: {user?.role || 'Unknown'}
        </Typography>
        
        <Box mt={3}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate('/')}
            sx={{ mr: 2 }}
          >
            Go to Dashboard
          </Button>
          
          <Button
            variant="outlined"
            onClick={() => navigate(-1)}
          >
            Go Back
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default UnauthorizedPage;
