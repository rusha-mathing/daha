import {type FC} from "react";
import {Card, CardContent, Typography, Button, Box, Stack, useTheme} from '@mui/material';
import Label from "./Label.tsx";
import {Flex} from "../../components/FlexGrid.tsx";
import {type Course as CourseInterface} from "../../../src/data/types.ts";
import DifficultyLabel from "./used/DifficultyLabel.tsx";
import SubjectLabel from "./used/SubjectLabel.tsx";

interface CourseProps {
    course: CourseInterface
}

const Course: FC<CourseProps> = ({course}) => {
    const theme = useTheme()
    return (
        <Card sx={{
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            transition: 'all 0.3s ease',
            borderRadius: {xs: '6px', sm: '8px'},
            overflow: 'visible',
            backgroundColor: theme.palette.background.paper,
            boxShadow: 'none',
            border: '1px solid' + theme.palette.grey["200"],
            '&:hover': {
                borderColor: theme.palette.primary.main,
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.04)',
            },
            position: 'relative',
            mb: {xs: 2, sm: 3},
            width: '100%'
        }}>
            <CardContent sx={{
                pt: {xs: 2.5, sm: 3, md: 3.5},
                pb: {xs: 1.5, sm: 2},
                flexGrow: 1,
                px: {xs: 2, sm: 2.5, md: 3},
                display: 'flex',
                flexDirection: 'column',
                gap: {xs: 1, sm: 1.5}
            }}>
                <Typography
                    component="div"
                    variant="h6"
                    sx={{
                        fontSize: {xs: '1.2rem', sm: '1.35rem', md: '1.5rem'},
                        letterSpacing: '-0.01em',
                        lineHeight: 1.2,
                        color: theme.palette.primary.main,
                        mb: {xs: 0.3, sm: 0.5}
                    }}
                >
                    {course.title}
                </Typography>
                <Typography
                    variant="h6"
                    sx={{
                        fontSize: {xs: '1rem', sm: '1.05rem', md: '1.1rem'},
                        mb: {xs: 0.5, sm: 1},
                        color: theme.palette.grey["700"]
                    }}
                >
                    {course.organization}
                </Typography>
                <Typography
                    variant="h6"
                    sx={{
                        fontSize: {xs: '1.2rem', sm: '1.25rem', md: '1.35rem'},
                        mb: {xs: 1.5, sm: 2},
                        color: theme.palette.text.primary,
                        letterSpacing: '-0.01em'
                    }}
                >
                    {course.start_date} — {course.end_date}
                </Typography>

                <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap sx={{mb: {xs: 1.5, sm: 2}}}>
                    {course.grades.map((grade) => {
                        return (
                            <Label
                                key={"grade_" + grade}
                                label={`${grade} класс`}
                                sx={{
                                    height: 'auto',
                                    py: {xs: 2, sm: 2.5},
                                    backgroundColor: theme.palette.grey["100"],
                                    color: theme.palette.grey['800']
                                }}
                            />
                        )
                    })}
                    <DifficultyLabel course={course}/>
                </Stack>

                <Box sx={{mb: {xs: 2, sm: 2.5, md: 3}}}>
                    <Typography
                        variant="body1"
                        sx={{
                            lineHeight: {xs: 1.5, sm: 1.6},
                            color: theme.palette.grey["800"],
                            fontSize: {xs: '0.95rem', sm: '1rem'}
                        }}
                    >
                        {course.description}
                    </Typography>
                </Box>

                <Box sx={{mb: {xs: 1.5, sm: 2}}}>
                    <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap sx={{mb: 0.5}}>
                        {course.subjects.map(subject => <SubjectLabel key={subject} subject={subject}/>)}
                    </Stack>
                </Box>
            </CardContent>
            <Flex sx={{
                justifyContent: 'flex-start',
                px: {xs: 2, sm: 2.5, md: 3},
                pb: {xs: 2, sm: 2.5, md: 3},
                mt: 'auto'
            }}>
                <Button
                    variant="contained"
                    href={course.url}
                    target="_blank"
                    rel="noopener"
                    sx={{
                        px: {xs: 3, sm: 3.5, md: 4},
                        py: {xs: 0.75, sm: 1},
                        fontSize: {xs: '0.9rem', sm: '0.95rem'},
                    }}
                >
                    Ссылка на курс
                </Button>
            </Flex>
        </Card>
    );
};

export default Course;
