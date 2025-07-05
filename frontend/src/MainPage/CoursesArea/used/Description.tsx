import {type FC} from 'react';
import {Typography, useTheme} from "@mui/material";
import {type Course} from "../../../types/course.ts"
import {useSubjectLookup} from "../../../hooks.ts";

interface DescriptionProps {
    course: Course;
}

const Description: FC<DescriptionProps> = ({course}) => {
    const theme = useTheme()
    const {lookup, isLoading, error} = useSubjectLookup()
    if (error) return <h1>error</h1>
    if (isLoading) return <h1>Loading...</h1>
    const getEnhancedDescription = (description: string) => {
        if (description.length > 150) return description;

        let formattedDescription = description;

        if (formattedDescription &&
            !formattedDescription.endsWith('.') &&
            !formattedDescription.endsWith('!') &&
            !formattedDescription.endsWith('?')) {
            formattedDescription += '.';
        }

        if (course.subjects && course.subjects.length > 0) {
            const primarySubject = course.subjects[0];
            const additions = lookup[primarySubject].additional_description;

            if (additions) {
                return `${formattedDescription} ${additions.join(' ')}`;
            }
        }
        return `${formattedDescription} Программа разработана ведущими специалистами с учетом современных требований отрасли. Участники получат актуальные знания и ценные практические навыки.`;
    };
    return (
        <Typography
            variant="body1"
            sx={{
                lineHeight: {xs: 1.5, sm: 1.6},
                color: theme.palette.grey["800"],
                fontSize: {xs: '0.95rem', sm: '1rem'}
            }}
        >
            {getEnhancedDescription(course.description)}
        </Typography>
    );
};

export default Description;