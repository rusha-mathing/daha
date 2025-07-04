import type {FC} from 'react';
import {Flex} from "./FlexGrid.tsx";
import type {ChildrenProps} from "../../src/data/types.ts";
import {useTheme} from "@mui/material";

const FilterItem: FC<ChildrenProps> = ({children}) => {
    const theme = useTheme();
    return (
        <Flex
            sx={{
                alignItems: 'center',
                justifyContent: 'flex-start',
                padding: '8px 12px',
                borderRadius: '12px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                flexShrink: 0,
                backgroundColor: theme.palette.background.default,
                color: theme.palette.text.primary,
                border: "1px solid #f00",
                '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: '0 2px 6px rgba(0, 0, 0, 0.05)',
                }
            }}
        >
            {children}
        </Flex>
    );
};

export default FilterItem;