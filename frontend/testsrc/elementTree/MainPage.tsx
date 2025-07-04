import {
    Container,
    Paper,
    Box,
    IconButton, useMediaQuery, type Theme, useTheme
} from '@mui/material';
import FilterAltIcon from '@mui/icons-material/FilterAlt';
import {type FC, useState} from 'react';
import FilterCard from './FilterCard/FilterCard.tsx';
import CoursesArea from "./CoursesArea/CoursesArea.tsx";
import {Flex, Grid} from "../components/FlexGrid.tsx";
import MobilePanel from "./MobilePanel/MobilePanel.tsx";

const MainPage: FC = () => {
    const theme = useTheme();
    const [mobilePanelOpen, setMobilePanelOpen] = useState(false);
    const isMobile = useMediaQuery((theme: Theme) => theme.breakpoints.down('md'));
    return (
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
                            <FilterCard onMobileCloseIconClick={() => setMobilePanelOpen(false)}/>
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
                        <CoursesArea/>
                    </Box>
                </Grid>
            </Flex>
            <MobilePanel
                open={isMobile && mobilePanelOpen}
                onClose={() => setMobilePanelOpen(false)}
            >
                <FilterCard onMobileCloseIconClick={() => setMobilePanelOpen(false)}/>
            </MobilePanel>
        </Container>
    );
};

export default MainPage;