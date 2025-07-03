import type {FC} from "react";
import {Box, SvgIcon, Typography} from "@mui/material";
import DynamicSvg from "../../../../components/DynamicSvg.tsx";
const svg = `<svg xmlns='http://www.w3.org/2000/svg'
     width='100%' height='100%' viewBox='0 0 24 24'>
    <path d="M20 9V7c0-1.1-.9-2-2-2h-3c0-1.66-1.34-3-3-3S9 3.34 9 5H6c-1.1 0-2 .9-2 2v2c-1.66 0-3 1.34-3 3s1.34 3 3 3v4c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-4c1.66 0 3-1.34 3-3s-1.34-3-3-3M7.5 11.5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5S9.83 13 9 13s-1.5-.67-1.5-1.5M16 17H8v-2h8zm-1-4c-.83 0-1.5-.67-1.5-1.5S14.17 10 15 10s1.5.67 1.5 1.5S15.83 13 15 13">

    </path>
</svg>
`
const Difficulty: FC = () => {
    return (
        <Box
            key="beginner"
            sx={{
                display: 'flex',
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
            <Box
                sx={{
                    width: 32,
                    height: 32,
                    mr: 1.5,
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backgroundColor: 'rgba(0, 0, 0, 0.08)', // "#002984"
                    color: "#64748b", // "#fff"
                }}
            >
                <SvgIcon fontSize="small">
                    <DynamicSvg svg={svg}/>
                </SvgIcon>
            </Box>

            <Typography
                sx={{
                    fontWeight: 500,
                    fontSize: '0.95rem',
                    color: "#1a202c",
                    flex: 1,
                    textAlign: 'left'
                }}
            >
                Начальный
            </Typography>
            {/*<Box*/}
            {/*    sx={{*/}
            {/*        width: 12,*/}
            {/*        height: 12,*/}
            {/*        borderRadius: '50%',*/}
            {/*        backgroundColor: "red",*/}
            {/*        ml: 1*/}
            {/*    }}*/}
            {/*/>*/}
        </Box>
    );
}

export default Difficulty;