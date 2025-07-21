import {type FC} from 'react';
import {Flex} from "../../components/FlexGrid.tsx";
import {useTheme} from "@mui/material";
import type {PassThroughProps} from "../../types";


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