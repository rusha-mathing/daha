import {type FC, useState} from 'react';
import {Typography, useTheme} from "@mui/material";
import Round from './Round.tsx';

interface GradeProps {
    clicked: boolean;
    grade: number | string;
    onClick?: (clicked: boolean) => void;
}

const Grade: FC<GradeProps> = ({grade, onClick, clicked}) => {
    const [stateClicked, setStateClicked] = useState(clicked);
    if (stateClicked != clicked) setStateClicked(clicked)
    const theme = useTheme();
    return (
        <div onClick={() => {
            if (onClick) onClick(!stateClicked)
            setStateClicked(!stateClicked)
        }}>
            <Round
                sx={{
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    flexShrink: 0,
                    backgroundColor: stateClicked ? theme.palette.primary.dark : theme.palette.background.default,
                    border: "1px solid " + theme.palette.grey["300"],
                    '&:hover': {
                        transform: 'translateY(-2px)',
                        boxShadow: '0 2px 6px rgba(0, 0, 0, 0.05)',
                    }
                }}>
                <Typography
                    variant="subtitle1"
                    sx={{
                        color: stateClicked ? theme.palette.background.default : theme.palette.grey["900"],
                        textAlign: 'center',
                    }}
                >
                    {grade}
                </Typography>
            </Round>
        </div>
    );
};

export default Grade;