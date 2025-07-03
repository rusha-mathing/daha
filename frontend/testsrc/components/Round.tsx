import {type FC} from 'react';
import {Flex} from "./FlexGrid.tsx";
import type {PassThroughProps} from "../../src/data/types.ts";


const Round: FC<PassThroughProps> = ({children, sx}) => {
    return (
        <Flex
            sx={{
                width: 34,
                height: 34,
                mr: 1.5,
                borderRadius: '50%',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: 'rgba(0, 0, 0, 0.08)', // "#002984"
                color: "#64748b", // "#fff"
                ...sx
            }}
        >
            {children}
        </Flex>
    );
};

export default Round;