import {type FC} from "react";
import {FormControl, FormLabel, Stack} from '@mui/material';
import Difficulty from "./Difficulty/Difficulty.tsx";

const Difficulties: FC = () => {
    return (
        <FormControl component="fieldset" variant="standard" sx={{width: '100%'}}>
            <FormLabel
                component="legend"
                sx={{
                    fontWeight: 600,
                    fontSize: '1rem',
                    color: "#1a202c",
                    mb: 1.5,
                    '&.Mui-focused': {
                        color: "#1a202c"
                    }
                }}
            >
                Уровень сложности
            </FormLabel>
            <Stack
                direction="column"
                spacing={1.5}
                sx={{
                    flexWrap: 'wrap',
                    justifyContent: 'flex-start'
                }}
            >
                <Difficulty/>
            </Stack>
        </FormControl>
    );
};

export default Difficulties;