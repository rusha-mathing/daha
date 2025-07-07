import {type FC} from "react";
import {Box, Button, Card, CardContent, Stack, Typography, useTheme} from '@mui/material';
import Label from "./Label.tsx";
import {Flex} from "../../components/FlexGrid.tsx";
import {type Course as CourseInterface} from "../../types/course.ts";
import UseDifficultyLabel from "./used/UseDifficultyLabel.tsx";
import UseSubjectLabel from "./used/UseSubjectLabel.tsx";
import UseDescription from "./used/UseDescription.tsx";
import {capitalize, formatDate, getEnhancedDescription} from "./funcs.ts";
import type {Subject} from "../../types/filters/subject.ts";
import type {Difficulty} from "../../types/filters/difficulty.ts";

interface Lookups {
    subjectLookup?: Record<string, Subject>;
    difficultyLookup?: Record<string, Difficulty>;
}

interface CourseProps {
    course: CourseInterface;
    lookups?: Lookups;
}


const Course: FC<CourseProps> = ({course, lookups}) => {
    const theme = useTheme()
    const startDate = formatDate(course.start_date)
    const endDate = formatDate(course.end_date)
    return (
        <Card sx={{
            // height: '100%',
            display: 'flex',
            flexDirection: 'column',
            transition: 'all 0.3s ease',
            borderRadius: {xs: '6px', sm: '8px'},
            overflow: 'visible',
            backgroundColor: theme.palette.background.paper,
            boxShadow: 'none',
            border: '1px solid' + theme.palette.grey["300"],
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
                        fontWeight: theme.typography.fontWeightBold,
                        fontSize: {xs: '1.2rem', sm: '1.35rem', md: '1.5rem'},
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
                {(startDate && endDate) &&
                    <Typography
                        variant="h6"
                        sx={{
                            fontSize: {xs: '1.2rem', sm: '1.25rem', md: '1.35rem'},
                            mb: {xs: 1.5, sm: 2},
                            color: theme.palette.text.primary,
                            letterSpacing: '-0.01em'
                        }}
                    >
                        {formatDate(course.start_date)} — {formatDate(course.end_date)}
                    </Typography>}
                {course.grades &&
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
                        {(!lookups || !(lookups?.difficultyLookup)) &&
                            <UseDifficultyLabel difficulty={course.difficulty}/>}
                        {lookups && lookups.difficultyLookup && lookups.difficultyLookup[course.difficulty]?.label &&
                            <Label
                                label={"Уровень: " + lookups.difficultyLookup[course.difficulty].label}
                                sx={{
                                    height: 'auto',
                                    py: {xs: 2, sm: 2.5},
                                    backgroundColor: theme.palette.primary.light + "10",
                                    color: theme.palette.primary.light,
                                }}/>}
                    </Stack>}
                {course.description && (!lookups || !(lookups?.subjectLookup)) &&
                    <Box sx={{mb: {xs: 2, sm: 2.5, md: 3}}}>
                        <UseDescription course={course}/>
                    </Box>}
                {course.description && lookups && lookups.subjectLookup &&
                    <Box sx={{mb: {xs: 2, sm: 2.5, md: 3}}}>
                        <Typography
                            variant="body1"
                            sx={{
                                lineHeight: {xs: 1.5, sm: 1.6},
                                color: theme.palette.grey["800"],
                                fontSize: {xs: '0.95rem', sm: '1rem'}
                            }}
                        >
                            {getEnhancedDescription(lookups.subjectLookup[course.subjects[0]], course.description)}
                        </Typography>
                    </Box>}

                <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap sx={{mb: 0.5}}>
                    {course.subjects && (!lookups || !(lookups?.subjectLookup)) && course.subjects.map(subject => // TODO: add filter for prioritizing first picked labels
                        <Box key={subject} sx={{mb: {xs: 1.5, sm: 2}}}>
                            <UseSubjectLabel
                                subject={subject}/>
                        </Box>)
                    }
                    {course.subjects && lookups && lookups.subjectLookup &&
                        course.subjects.map(subject =>
                            lookups.subjectLookup![subject]?.label && <Box key={subject} sx={{mb: {xs: 1.5, sm: 2}}}>
                                <Label
                                    label={capitalize(lookups.subjectLookup![subject].label)}
                                    sx={{
                                        mb: 0.75,
                                        fontSize: {xs: '0.85rem', sm: '0.9rem'},
                                        backgroundColor: lookups.subjectLookup![subject].color + "10",
                                        color: lookups.subjectLookup![subject].color,
                                        height: {xs: '28px', sm: '32px'},
                                        px: {xs: 0.5, sm: 1}
                                    }}
                                />
                            </Box>)
                    }
                </Stack>
            </CardContent>
            <Flex sx={{
                justifyContent: 'flex-start',
                px: {xs: 2, sm: 2.5, md: 3},
                pb: {xs: 2, sm: 2.5, md: 3},
                mt: 'auto'
            }}>
                <Button
                    variant="contained"
                    {...(course.url ? {
                        href: course.url,
                        target: "_blank",
                        rel: "noopener"
                    } : {})}
                    sx={{
                        borderRadius: "5px",
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
