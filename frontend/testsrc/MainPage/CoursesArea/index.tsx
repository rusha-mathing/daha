import {type FC} from 'react';
import {Box, Typography, useTheme} from '@mui/material';
import Course from './Course';
import {Flex, Grid} from '../../components/FlexGrid';
import {useCourses} from "../../hooks.ts";


const CoursesArea: FC = () => {
    const theme = useTheme();
    const {data, isLoading, error} = useCourses();
    if (isLoading) {
        return <h1>loading</h1>
    }
    if (error) {
        return <h1>error</h1>
    }
    const courses = data!;
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
                >
                    Найдено возможностей: {courses.length}
                </Typography>
            </Flex>
            {courses.length ? (
                <Grid sx={{
                    gridTemplateColumns: '1fr',
                    gap: {xs: 2, sm: 3, md: 4},
                    width: '100%',
                    mx: 'auto'
                }}>
                    {courses.map((course) => {
                        return <Course key={course.id} course={course}/>
                    })}
                </Grid>
            ) : (
                <Box sx={{
                    py: {xs: 4, md: 6},
                    px: 2,
                    border: '1px dashed ' + theme.palette.grey["300"],
                    borderRadius: '8px',
                    backgroundColor: theme.palette.grey['300'] + "20"
                }}>
                    <Typography
                        variant="body1"
                        color="text.secondary"
                        align="center"
                        sx={{fontSize: {xs: '0.95rem', sm: '1rem'}}}
                    >
                        По вашему запросу не найдено возможностей. Попробуйте изменить параметры фильтрации.
                    </Typography>
                </Box>
            )}


        </Box>
    );
};

export default CoursesArea;