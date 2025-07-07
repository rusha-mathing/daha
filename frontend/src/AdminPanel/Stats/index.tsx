import {type FC} from 'react';
import {Grid} from "@mui/material";
import StatItem from "./StatItem.tsx";

const Stats: FC = () => {
    return (
        <Grid container spacing={3} sx={{mb: 4}}>
            <StatItem/>
            <StatItem/>
            <StatItem/>
            <StatItem/>
        </Grid>
    );
};

export default Stats;