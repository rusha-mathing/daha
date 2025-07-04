import {type FC} from 'react';
import {Flex} from "./FlexGrid.tsx";
import type {PassThroughProps} from "../../src/data/types.ts";
import {useTheme} from "@mui/material";


const Round: FC<PassThroughProps> = ({children, sx}) => {
    const theme = useTheme()
    return (
        <Flex
            sx={{
                width: 32,
                height: 32,
                mr: 1.5,
                borderRadius: '50%',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: theme.palette.grey["200"],
                color: theme.palette.grey["600"],
                ...sx
            }}
        >
            {children}
        </Flex>
    );
};

export default Round;