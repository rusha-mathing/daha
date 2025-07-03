import type {FC} from 'react';
import Box from '@mui/material/Box';
import type {PassThroughProps} from "../../src/data/types.ts";

export const Flex: FC<PassThroughProps> = ({
                                               sx,
                                               children,
                                               ...props
                                           }) => {
    return (
        <Box
            sx={{
                display: 'flex',
                ...sx,
            }}
            {...props}
        >
            {children}
        </Box>
    );
};


export const Grid: FC<PassThroughProps> = ({
                                               sx = undefined,
                                               children,
                                               ...props
                                           }) => {
    return (
        <Box
            sx={{
                display: 'grid',
                ...sx,
            }}
            {...props}
        >
            {children}
        </Box>
    );
};