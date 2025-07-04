import type {FC} from "react";
import {Box, Typography, useTheme} from "@mui/material";
import DynamicSvg from "../../components/DynamicSvg.tsx";
import Round from "./Round.tsx";
import {Flex} from "../../components/FlexGrid.tsx";

const svg = `<svg xmlns='http://www.w3.org/2000/svg'
     width='100%' height='100%' viewBox='0 0 24 24'>
    <path d="M20 9V7c0-1.1-.9-2-2-2h-3c0-1.66-1.34-3-3-3S9 3.34 9 5H6c-1.1 0-2 .9-2 2v2c-1.66 0-3 1.34-3 3s1.34 3 3 3v4c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-4c1.66 0 3-1.34 3-3s-1.34-3-3-3M7.5 11.5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5S9.83 13 9 13s-1.5-.67-1.5-1.5M16 17H8v-2h8zm-1-4c-.83 0-1.5-.67-1.5-1.5S14.17 10 15 10s1.5.67 1.5 1.5S15.83 13 15 13">

    </path>
</svg>
`
const FilterUnit: FC = () => {
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
            }}>
            <Round>
                <DynamicSvg fontSize="small" svg={svg}/>
            </Round>

            <Typography
                variant='body2'
                sx={{
                    flex: 1,
                    textAlign: 'left'
                }}
            >
                Искусственный интеллект
            </Typography>
            <Box
                sx={{
                    width: 12,
                    height: 12,
                    borderRadius: '50%',
                    backgroundColor: "red",
                    ml: 1
                }}
            />
        </Flex>
    );
}

export default FilterUnit;