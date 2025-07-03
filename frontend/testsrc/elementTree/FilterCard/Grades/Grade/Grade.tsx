import {type FC} from 'react';
import {Typography} from "@mui/material";
import Round from '../../../../components/Round.tsx';

const Grade: FC = () => {
    return (
        <Round sx={{
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            flexShrink: 0,
            '&:hover': {
                backgroundColor: "gray", // "#002984"
                transform: 'translateY(-2px)',
                boxShadow: '0 2px 6px rgba(0, 0, 0, 0.05)',
            }
        }}>
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
        </Round>
    );
};

export default Grade;