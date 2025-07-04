import {type FC, useState} from 'react';
import {Typography, useTheme} from "@mui/material";
import Round from './Round.tsx';

interface GradeProps {
    grade: number | string;
}

const Grade: FC<GradeProps> = ({grade}) => {
    const [clicked, setClicked] = useState(false);
    const theme = useTheme();
    return (
        <Round
            onClick={() => setClicked(!clicked)}
            sx={{
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
                {grade}
            </Typography>
        </Round>
    );
};

export default Grade;