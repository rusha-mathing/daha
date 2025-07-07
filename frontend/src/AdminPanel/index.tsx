import {type FC, useState} from 'react';
import {Flex} from "../components/FlexGrid"
import {Card, CardContent, CardHeader, Drawer, Typography} from '@mui/material';
import LeftSideMenu from "./LeftSideMenu";
import Stats from "./Stats";
import {
    Box,
    Container
} from "@mui/material";
import type {PageItem} from "../types/admintypes.ts";
import SchoolIcon from "@mui/icons-material/School";
import SubjectForm from "./used/SubjectForm";
import DifficultyForm from "./used/DifficultyForm";

const AdminPanel: FC = () => {
    const components: PageItem[] = [
        {
            label: "Subjects",
            icon: <SchoolIcon/>,
            component: <SubjectForm/>
        }, {
            label: "Difficulties",
            icon: <SchoolIcon/>,
            component: <DifficultyForm/>
        },
    ]
    const [component, setComponent] = useState(components[0]);

    return (
        <Flex sx={{minHeight: '100vh', backgroundColor: 'background.default'}}>
            <Drawer
                variant="permanent"
                sx={{
                    display: {xs: 'none', md: 'flex'},
                    '& .MuiDrawer-paper': {width: 280, boxSizing: 'border-box'},
                }}
                open
            >
                <LeftSideMenu setComponent={setComponent} pageItems={components}/>
            </Drawer>
            <Flex sx={{flexGrow: 1, flexDirection: 'column', ml: {md: '280px'}}}>
                <Box sx={{flexGrow: 1, p: 3}}>
                    <Container maxWidth="xl">
                        <Stats/>
                        <Card sx={{borderRadius: 3, overflow: 'hidden'}}>
                            <CardHeader
                                title={
                                    <Box sx={{display: 'flex', alignItems: 'center', gap: 2}}>
                                        {component.icon}
                                        <Typography variant="h5" fontWeight="600"
                                                    sx={{transform: "translate(0, 25%)",}}>
                                            {component.label}
                                        </Typography>
                                    </Box>
                                }
                                sx={{
                                    backgroundColor: 'background.default',
                                    borderBottom: '1px solid',
                                    borderColor: 'divider',
                                }}
                            />
                            <CardContent sx={{p: 4}}>
                                <Box>
                                    {component.component}
                                </Box>
                            </CardContent>
                        </Card>
                    </Container>
                </Box>
            </Flex>
        </Flex>
    );
};

export default AdminPanel;