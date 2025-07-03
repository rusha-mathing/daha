import {
    Container,
    Paper,
    Box,
    Drawer,
    IconButton, useMediaQuery, type Theme
} from '@mui/material';
import FilterAltIcon from '@mui/icons-material/FilterAlt';
import type {FC} from 'react';
import FilterCard from './FilterCard/FilterCard.tsx';
import CoursesArea from "./CoursesArea/CoursesArea.tsx";

const MainPage: FC = () => {
    const isMobile = useMediaQuery((theme: Theme) => theme.breakpoints.down('md'));
    return (
        <Container maxWidth="xl" sx={{
            mt: {xs: 2, sm: 3, md: 4, lg: 5},
            mb: {xs: 3, sm: 4, md: 5, lg: 6},
            px: {xs: 1.5, sm: 2, md: 3, lg: 4}
        }}>
            <Box sx={{
                display: 'flex',
                flexDirection: 'column',
                gap: {xs: 2, sm: 3, md: 4},
                width: '100%'
            }}>
                <Box sx={{
                    display: 'grid',
                    gridTemplateColumns: {xs: '1fr', md: '280px 1fr', lg: '320px 1fr'},
                    gap: {xs: 2, sm: 2.5, md: 3, lg: 4},
                    width: '100%',
                    mx: 'auto'
                }}>
                    {!isMobile ? (
                        <Paper
                            elevation={0}
                            sx={{
                                p: 0,
                                height: 'fit-content',
                                borderRadius: {xs: 2, sm: 3},
                                border: `1px solid lightblue`,
                                overflow: 'hidden',
                                position: 'sticky',
                                top: '20px',
                                alignSelf: 'start'
                            }}
                        >
                            <FilterCard/>
                        </Paper>
                    ) : (
                        <Box sx={{display: 'flex', justifyContent: 'flex-end', mb: 1}}>
                            <IconButton
                                color="primary"
                                sx={{
                                    border: `1px solid blue`,
                                    borderRadius: 2,
                                    boxShadow: '0 2px 4px rgba(0,0,0,0.04)'
                                }}
                            >
                                <FilterAltIcon/>
                            </IconButton>
                        </Box>
                    )}

                    <Box
                        sx={{
                            gridColumn: {xs: '1', md: '2'},
                            minHeight: {xs: '50vh', sm: '60vh'},
                            width: '100%',
                            overflow: 'visible'
                        }}
                    >
                        <CoursesArea/>
                    </Box>
                </Box>
            </Box>
            <Drawer
                anchor="left"
                open={isMobile}
                slotProps={
                    {
                        paper: {
                            sx: {
                                width: {xs: '85%', sm: 350}, // Адаптивная ширина для разных экранов
                                borderRadius: '0 16px 16px 0',
                                boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                                maxWidth: '100vw'
                            }
                        }
                    }
                }
            >
                <FilterCard/>
            </Drawer>
        </Container>
    );
};

export default MainPage;