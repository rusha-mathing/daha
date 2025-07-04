import {type FC} from 'react';
import {Typography, useTheme} from "@mui/material";
import Round from './Round.tsx';

const Grade: FC = () => {
    const theme = useTheme();
    return (
        <Round sx={{
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
            <Typography
                variant="subtitle1"
                sx={{
                    color: theme.palette.grey["900"],
                    textAlign: 'center',
                }}
            >
                7
            </Typography>
        </Round>
    );
};

export default Grade;