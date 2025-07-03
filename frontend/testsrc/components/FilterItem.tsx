import type {ReactNode, FC} from 'react';
import {Flex} from "./FlexGrid.tsx";

interface FilterItemProps {
    children?: ReactNode;
}

const FilterItem: FC<FilterItemProps> = ({children}) => {

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
                backgroundColor: 'gray', // "#3f51b5"
                color: "#1a202c", // "#fff"
                border: "#f00",
                '&:hover': {
                    backgroundColor: "gray", // "#002984"
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