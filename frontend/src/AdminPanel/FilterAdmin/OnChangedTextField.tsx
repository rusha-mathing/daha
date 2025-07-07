import { type FC, useState, type ChangeEvent } from 'react';
import { TextField, type TextFieldProps } from '@mui/material';

const OnChangedTextField: FC<TextFieldProps> = (props) => {
    const [text, setText] = useState<string>('');

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setText(e.target.value);
        if (props.onChange) {
            props.onChange(e);
        }
    };

    return <TextField {...props} value={text} onChange={handleChange} />;
};

export default OnChangedTextField;