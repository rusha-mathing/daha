import { AppBar, Toolbar, Typography, Container, Box, useTheme } from '@mui/material';
import ScienceIcon from '@mui/icons-material/Science';

const Header: React.FC = () => {
  const theme = useTheme();
  
  return (
    <AppBar 
      position="sticky" 
      color="default"
      elevation={0}
      sx={{ 
        backdropFilter: 'blur(10px)',
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        borderBottom: '1px solid rgba(0, 0, 0, 0.05)'
      }}
    >
      <Container maxWidth="lg">
        <Toolbar disableGutters sx={{ py: 1.5 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <ScienceIcon 
              sx={{ 
                fontSize: { xs: '1.8rem', md: '2.2rem' },
                mr: 2,
                color: theme.palette.primary.main
              }} 
            />
            <Typography
              variant="h5"
              component="div"
              sx={{
                fontFamily: "'Inter', sans-serif",
                fontWeight: 700,
                letterSpacing: '-0.02em',
                background: `linear-gradient(45deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              ВСЕЛЕННАЯ ЗНАНИЙ
            </Typography>
          </Box>

          <Box sx={{ flexGrow: 1 }} />
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header;