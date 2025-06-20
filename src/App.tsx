import { CssBaseline, Box, ThemeProvider } from '@mui/material';
import MainPage from './components/layout/MainPage';
import theme from './theme/theme';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    minHeight: '100vh',
                    width: '100%',
                    maxWidth: '100vw',
                    overflowX: 'hidden'
                }}
            >
                <Box sx={{ flex: '1 0 auto', py: { xs: 2, sm: 3, md: 4 }, width: '100%' }}>
                    <MainPage />
                </Box>
            </Box>
        </ThemeProvider>
    );
}

export default App;
