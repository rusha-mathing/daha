import {type FC} from "react";
import {FormControl, FormLabel, Stack} from '@mui/material';
import Subject from "./Subject/Subject.tsx";

const Subjects: FC = () => {
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
                Направления
            </FormLabel>
            <Stack
                direction="column"
                spacing={1.5}
                sx={{
                    flexWrap: 'wrap',
                    justifyContent: 'flex-start'
                }}
            >
                <Subject/>
                <Subject/>
                <Subject/>
                <Subject/>
                <Subject/>
                <Subject/>
                <Subject/>
                <Subject/>
                <Subject/>
            </Stack>
        </FormControl>
    );
};

export default Subjects;