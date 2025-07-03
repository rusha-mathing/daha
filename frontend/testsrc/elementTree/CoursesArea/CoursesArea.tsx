import {type FC} from 'react';
import {Box, Typography} from '@mui/material';
import Course from './Course/Course';
import { Flex, Grid } from '../../components/FlexGrid';

const CoursesArea: FC = () => {
    return (
        <Box>
            <Flex sx={{
                justifyContent: 'space-between',
                alignItems: 'center',
                mb: {xs: 1.5, sm: 2, md: 3},
                px: {xs: 0.5, sm: 1}
            }}>
                <Typography
                    variant="h6"
                    component="div"
                    sx={{
                        fontSize: {xs: '1rem', sm: '1.1rem', md: '1.25rem'},
                        fontWeight: 600
                    }}
                >
                    Найдено возможностей: 1
                </Typography>
            </Flex>

            <Grid sx={{
                gridTemplateColumns: '1fr',
                gap: {xs: 2, sm: 3, md: 4},
                width: '100%',
                mx: 'auto'
            }}>
                <Course/>
                <Course/>
            </Grid>
            {/*<Box sx={{*/}
            {/*    py: {xs: 4, md: 6},*/}
            {/*    px: 2,*/}
            {/*    border: '1px dashed #ddd',*/}
            {/*    borderRadius: '8px',*/}
            {/*    backgroundColor: '#fafafa'*/}
            {/*}}>*/}
            {/*    <Typography*/}
            {/*        variant="body1"*/}
            {/*        color="text.secondary"*/}
            {/*        align="center"*/}
            {/*        sx={{fontSize: {xs: '0.95rem', sm: '1rem'}}}*/}
            {/*    >*/}
            {/*        По вашему запросу не найдено возможностей. Попробуйте изменить параметры фильтрации.*/}
            {/*    </Typography>*/}
            {/*</Box>*/}
        </Box>
    );
};

export default CoursesArea;