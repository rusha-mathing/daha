import type {ReactNode, FC} from 'react';
import {FormControl, FormLabel, Stack} from "@mui/material";

interface FilterProps {
    title: string,
    children?: ReactNode,
}

const Filter: FC<FilterProps> = ({title, children}) => {
    return (
        <FormControl component="fieldset" variant="standard" sx={{width: '100%'}}>
            <FormLabel
                component="legend"
                sx={{
                    fontWeight: 600,
                    fontSize: '1rem',
                    color: "#1a202c",
                    mb: 1.5,
                    '&.Mui-focused': {
                        color: "#1a202c"
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