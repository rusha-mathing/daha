import {type FC} from 'react';
import {Box, Typography} from "@mui/material";

const Grade: FC = () => {
    return (
        <Box
            key="7"
            sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: 0,
                borderRadius: '50%',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                width: '34px',
                height: '34px',
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
            <Typography
                sx={{
                    fontWeight: 600,
                    fontSize: '0.95rem',
                    color: "#1a202c",
                    textAlign: 'center',
                }}
            >
                7
            </Typography>
        </Box>
    );
};

export default Grade;