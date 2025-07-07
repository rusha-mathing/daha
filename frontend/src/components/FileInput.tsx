import {Button, TextField} from '@mui/material';
import {type FC, useState, type ChangeEvent} from 'react';
import {Flex} from './FlexGrid';

interface FileInputProps {
    setFile: (val: string) => void;
}

//TODO useCallback
const FileInput: FC<FileInputProps> = ({setFile}) => {
    const [url, setUrl] = useState<string>('');

    const handleUrlChange = (event: ChangeEvent<HTMLInputElement>) => {
        const newUrl = event.target.value;
        setUrl(newUrl);
        setFile(newUrl);
    };

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            const fileUrl = URL.createObjectURL(file);
            setFile(fileUrl);
        }
    };

    return (
        <Flex sx={{gap: 2, maxWidth: 400}}>
            <TextField
                sx={{maxWidth: 300, width: "100%"}}
                label="File URL"
                variant="outlined"
                value={url}
                onChange={handleUrlChange}
                fullWidth
                placeholder="https://example.com/file"
            />
            <Button
                variant="contained"
                component="label"
                sx={{maxWidth: 300, width: "50%"}}
            >
                Upload File
                <input
                    type="file"
                    hidden
                    onChange={handleFileChange}
                />
            </Button>
        </Flex>
    );
};

export default FileInput;