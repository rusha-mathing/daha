import {type FC} from 'react';
import {FormControl, FormLabel, Stack} from '@mui/material';
import Grade from './Grade/Grade';

const Grades: FC = () => {
    return (
        <FormControl component="fieldset" variant="standard" sx={{width: '100%'}}>
            <FormLabel
                component="legend"
                sx={{
                    fontWeight: 600,
                    fontSize: '1rem',
                    color: '#1a202c',
                    mb: 1.5,
                    '&.Mui-focused': {
                        color: "#1a202c"
                    }
                }}
            >
                Классы
            </FormLabel>
            <Stack
                direction='row'
                spacing={1.5}
                sx={{
                    flexWrap: 'nowrap',
                    justifyContent: 'space-between',
                }}
            >
                <Grade/>
            </Stack>
        </FormControl>
    );
};

export default Grades;