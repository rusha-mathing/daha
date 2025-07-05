import type {ReactNode, FC} from 'react';
import {FormControl, FormLabel, Stack, useTheme} from "@mui/material";

interface FilterProps {
    title: string,
    direction?: "column" | "row" | "row-reverse" | "column-reverse"
    children?: ReactNode,
}

const Filter: FC<FilterProps> = ({title, direction = "column", children}) => {
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
                }}
            >
                {title}
            </FormLabel>
            <Stack
                direction={direction}
                spacing={1.5}
                sx={{
                    flexWrap: direction === 'row' ? 'nowrap' : 'wrap',
                    justifyContent: direction === 'row' ? 'space-between' : 'flex-start'
                }}
            >
                {children}
            </Stack>
        </FormControl>
    );
};

export default Filter;