import {type FC, useState} from "react";
import {Box, Typography, useTheme} from "@mui/material";
import DynamicSvg from "../../components/DynamicSvg.tsx";
import Round from "./Round.tsx";
import {Flex} from "../../components/FlexGrid.tsx";
import {type Filter as FilterInterface} from "../../types/filters";


interface FilterUnitProps {
    clicked: boolean;
    unit: FilterInterface;
    onClick?: (clicked: boolean) => void;
}

const FilterUnit: FC<FilterUnitProps> = ({unit, onClick, clicked}) => {
    const [stateClicked, setStateClicked] = useState(clicked);
    if (clicked != stateClicked) setStateClicked(clicked)
    const theme = useTheme();
    return (
        <Flex
            onClick={() => {
                if (onClick) onClick(!stateClicked);
                setStateClicked(!stateClicked)
            }}
            sx={{
                alignItems: 'center',
                justifyContent: 'flex-start',
                padding: '8px 12px',
                borderRadius: '12px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                flexShrink: 0,
                backgroundColor: stateClicked ? unit.color + "20" : theme.palette.background.default,
                color: stateClicked ? unit.color : theme.palette.text.primary,
                border: '1px solid ' + (stateClicked ? `${unit.color}50` : `${theme.palette.text.primary}20`),
                '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: '0 2px 6px rgba(0, 0, 0, 0.05)',
                }
            }}>
            <Round sx={{
                backgroundColor: stateClicked ? unit.color : theme.palette.grey["200"]
            }}>
                <DynamicSvg
                    fontSize="small" svg={unit.icon}
                    sx={{
                        color: stateClicked ? theme.palette.background.default : undefined
                    }}
                />
            </Round>

            <Typography
                variant='body2'
                sx={{
                    flex: 1,
                    textAlign: 'left'
                }}
            >
                {unit.label.charAt(0).toUpperCase() + unit.label.slice(1)}
            </Typography>
            {stateClicked && <Box
                sx={{
                    width: 12,
                    height: 12,
                    borderRadius: '50%',
                    backgroundColor: unit.color,
                    ml: 1
                }}
            />}
        </Flex>
    );
}

export default FilterUnit;