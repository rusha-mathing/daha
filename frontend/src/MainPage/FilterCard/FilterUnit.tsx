import {type FC} from "react";
import {Box, Typography, useTheme} from "@mui/material";
import DynamicSvg from "../../components/DynamicSvg.tsx";
import Round from "./Round.tsx";
import {Flex} from "../../components/FlexGrid.tsx";
import {type Filter as FilterInterface} from "../../types/filters";


interface FilterUnitProps {
    clicked: boolean;
    unit: FilterInterface;
    onClick?: () => void;
}

const FilterUnit: FC<FilterUnitProps> = ({unit, onClick, clicked}) => {
    const theme = useTheme();
    return (
        <Flex
            onClick={onClick ? () => onClick() : undefined}
            sx={{
                alignItems: 'center',
                justifyContent: 'flex-start',
                padding: '8px 12px',
                borderRadius: '12px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                flexShrink: 0,
                backgroundColor: clicked ? unit.color + "20" : theme.palette.grey["100"] + "80",
                color: clicked ? unit.color : theme.palette.text.primary,
                border: '1px solid ' + (clicked ? `${unit.color}50` : `${theme.palette.grey["300"]}`),
                '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: '0 2px 6px rgba(0, 0, 0, 0.05)',
                }
            }}>
            <Round sx={{
                backgroundColor: clicked ? unit.color : theme.palette.grey["400"] + "50"
            }}>
                <DynamicSvg
                    fontSize="small" svg={unit.icon}
                    sx={{
                        color: clicked ? theme.palette.background.default : theme.palette.text.primary + "95"
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
            {clicked && <Box
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