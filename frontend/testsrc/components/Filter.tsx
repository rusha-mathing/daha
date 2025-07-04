import type {ReactNode, FC} from 'react';
import {FormControl, FormLabel, Stack, useTheme} from "@mui/material";

interface FilterProps {
    title: string,
    children?: ReactNode,
}

const Filter: FC<FilterProps> = ({title, children}) => {
    const theme = useTheme();
    return (
        <FormControl component="fieldset" variant="standard" sx={{width: '100%'}}>
            <FormLabel
                component="legend"
                sx={{
                    fontWeight: theme.typography.subtitle1.fontWeight,
                    fontSize: theme.typography.subtitle1.fontSize,
                    color: theme.palette.text.primary,
                    mb: 1.5,
                    '&.Mui-focused': {
                        color: theme.palette.text.primary
                    }
                }}
            >
                {title}
            </FormLabel>
            <Stack
                direction="column"
                spacing={1.5}
                sx={{
                    flexWrap: 'wrap',
                    justifyContent: 'flex-start'
                }}
            >
                {children}
            </Stack>
        </FormControl>
    );
};

export default Filter;