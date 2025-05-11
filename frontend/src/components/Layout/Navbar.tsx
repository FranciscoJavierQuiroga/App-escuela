// src/components/Layout/Navbar.tsx
import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box, IconButton, Menu, MenuItem, Avatar } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import MenuIcon from '@mui/icons-material/Menu';

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [mobileMenuAnchorEl, setMobileMenuAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMobileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setMobileMenuAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setMobileMenuAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleMenuClose();
    navigate('/login');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            flexGrow: 1,
            textDecoration: 'none',
            color: 'inherit',
            fontWeight: 'bold',
          }}
        >
          School Management System
        </Typography>

        {/* Desktop menu */}
        <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
          <Button color="inherit" component={RouterLink} to="/">
            Home
          </Button>
          
          {isAuthenticated ? (
            <>
              {user?.role === 'ADMIN' && (
                <>
                  <Button color="inherit" component={RouterLink} to="/students">
                    Students
                  </Button>
                  <Button color="inherit" component={RouterLink} to="/teachers">
                    Teachers
                  </Button>
                </>
              )}
              
              <Button color="inherit" component={RouterLink} to="/courses">
                Courses
              </Button>
              
              {user?.role === 'STUDENT' && (
                <Button color="inherit" component={RouterLink} to="/my-grades">
                  My Grades
                </Button>
              )}
              
              <IconButton
                edge="end"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleProfileMenuOpen}
                color="inherit"
              >
                <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
                  {user?.first_name?.[0] || user?.email?.[0]}
                </Avatar>
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
              >
                <MenuItem onClick={() => { handleMenuClose(); navigate('/profile'); }}>
                  Profile
                </MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </>
          ) : (
            <>
              <Button color="inherit" component={RouterLink} to="/login">
                Login
              </Button>
            </>
          )}
        </Box>

        {/* Mobile menu icon */}
        <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
          <IconButton
            size="large"
            aria-label="menu"
            aria-controls="menu-mobile"
            aria-haspopup="true"
            onClick={handleMobileMenuOpen}
            color="inherit"
          >
            <MenuIcon />
          </IconButton>
          <Menu
            id="menu-mobile"
            anchorEl={mobileMenuAnchorEl}
            keepMounted
            open={Boolean(mobileMenuAnchorEl)}
            onClose={handleMenuClose}
          >
            <MenuItem onClick={() => { handleMenuClose(); navigate('/'); }}>
              Home
            </MenuItem>
            
            {isAuthenticated ? (
              <>
                {user?.role === 'ADMIN' && (
                  <>
                    <MenuItem onClick={() => { handleMenuClose(); navigate('/students'); }}>
                      Students
                    </MenuItem>
                    <MenuItem onClick={() => { handleMenuClose(); navigate('/teachers'); }}>
                      Teachers
                    </MenuItem>
                  </>
                )}
                
                <MenuItem onClick={() => { handleMenuClose(); navigate('/courses'); }}>
                  Courses
                </MenuItem>
                
                {user?.role === 'STUDENT' && (
                  <MenuItem onClick={() => { handleMenuClose(); navigate('/my-grades'); }}>
                    My Grades
                  </MenuItem>
                )}
                
                <MenuItem onClick={() => { handleMenuClose(); navigate('/profile'); }}>
                  Profile
                </MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </>
            ) : (
              <MenuItem onClick={() => { handleMenuClose(); navigate('/login'); }}>
                Login
              </MenuItem>
            )}
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
