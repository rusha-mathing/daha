import {type FC} from 'react';
import {Typography, useTheme} from "@mui/material";
import {type Course} from "../../../types/course.ts"
import {useSubjectLookup} from "../../../hooks.ts";
import {getEnhancedDescription} from "../funcs.ts";

interface DescriptionProps {
    course: Course;
}

const UseDescription: FC<DescriptionProps> = ({course}) => {
    const theme = useTheme()
    const {lookup, isLoading, error} = useSubjectLookup()
    if (error) return <h1>error</h1>
    if (isLoading) return <h1>Loading...</h1>
    return (
        <Typography
            variant="body1"
            sx={{
                lineHeight: {xs: 1.5, sm: 1.6},
                color: theme.palette.grey["800"],
                fontSize: {xs: '0.95rem', sm: '1rem'}
            }}
        >
            {getEnhancedDescription(lookup[course.subjects[0]], course.description)}
        </Typography>
    );
};

export default UseDescription;