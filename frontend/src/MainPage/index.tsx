import {
    Container,
    Paper,
    Box,
    IconButton, useMediaQuery, type Theme, useTheme, Typography, Button
} from '@mui/material';
import FilterAltIcon from '@mui/icons-material/FilterAlt';
import {type FC, useState} from 'react';
import FilterCard from './FilterCard';
import CoursesArea from "./CoursesArea";
import {Flex, Grid} from "../components/FlexGrid.tsx";
import MobilePanel from "./MobilePanel";
import type {SDGFilters} from "../types/filters";
import {Link} from "react-router-dom";


const MainPage: FC = () => {
    const theme = useTheme();
    const [mobilePanelOpen, setMobilePanelOpen] = useState(false);
    const [filters, setFilters] = useState<SDGFilters>({
        subjectTypes: [],
        difficultyTypes: [],
        grades: [],
    });
    const isMobile = useMediaQuery((theme: Theme) => theme.breakpoints.down('md'));
    return (
        <Flex
            sx={{
                flexDirection: 'column',
                minHeight: '100vh',
                width: '100%',
                maxWidth: '100vw',
                overflowX: 'hidden'
            }}
        >
            <Flex sx={{
                flexDirection: "column",
                backgroundColor: "red",
                width: '100%',
                justifyContent: "center",
                alignItems: "center",
                textAlign: "center",
                position: "fixed",
                padding: "20px",
                zIndex: 9999 - 1,
            }}>
                <Typography variant="h3" sx={{color: "white", zIndex: 9999}}>
                    WARNING: Development build DO NOT put on production!
                </Typography>
                <Flex sx={{width: "100%", justifyContent: "flex-end", pr: "20px"}}>
                    <div></div>
                    <Link to="/admin">
                        <Button
                            variant="contained">
                            Admin Panel
                        </Button>
                    </Link>
                </Flex>
            </Flex>
            <Box sx={{flex: '1 0 auto', py: {xs: 2, sm: 3, md: 4}, width: '100%'}}>
                <Container maxWidth="xl" sx={{
                    mt: {xs: 2, sm: 3, md: 4, lg: 5},
                    mb: {xs: 3, sm: 4, md: 5, lg: 6},
                    px: {xs: 1.5, sm: 2, md: 3, lg: 4}
                }}>
                    <Flex sx={{
                        flexDirection: 'column',
                        gap: {xs: 2, sm: 3, md: 4},
                        width: '100%'
                    }}>
                        <Grid sx={{
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
                                        border: '1px solid' + theme.palette.grey["200"],
                                        overflow: 'hidden',
                                        position: 'sticky',
                                        top: '20px',
                                        alignSelf: 'start'
                                    }}
                                >
                                    <FilterCard filters={filters}
                                                setFilters={setFilters}
                                                onMobileCloseIconClick={() => setMobilePanelOpen(false)}/>
                                </Paper>
                            ) : (
                                <Flex sx={{justifyContent: 'flex-end', mb: 1}}>
                                    <IconButton
                                        color="primary"
                                        onClick={() => setMobilePanelOpen(true)}
                                        sx={{
                                            border: `1px solid blue`,
                                            borderRadius: 2,
                                            boxShadow: '0 2px 4px rgba(0,0,0,0.04)'
                                        }}
                                    >
                                        <FilterAltIcon/>
                                    </IconButton>
                                </Flex>
                            )}

                            <Box
                                sx={{
                                    gridColumn: {xs: '1', md: '2'},
                                    minHeight: {xs: '50vh', sm: '60vh'},
                                    width: '100%',
                                    overflow: 'visible'
                                }}
                            >
                                <CoursesArea filters={filters}/>
                            </Box>
                        </Grid>
                    </Flex>
                    <MobilePanel
                        open={isMobile && mobilePanelOpen}
                        onClose={() => setMobilePanelOpen(false)}
                    >
                        <FilterCard filters={filters} setFilters={setFilters}
                                    onMobileCloseIconClick={() => setMobilePanelOpen(false)}/>
                    </MobilePanel>
                </Container>
            </Box>
        </Flex>
    );
};

export default MainPage;