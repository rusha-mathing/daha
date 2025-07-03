import {type FC} from 'react';
import {Chip, type SxProps} from "@mui/material";

interface LabelProps {
    label: string;
    sx: SxProps;
}

const Label: FC<LabelProps> = ({
                                   label,
                                   sx
                               }) => {
    return (
        <Chip
            label={label}
            size="medium"
            sx={{
                mb: 1,
                borderRadius: {xs: '4px', sm: '6px'},
                px: {xs: 1, sm: 1.5},
                fontWeight: 500,
                fontSize: {xs: '0.85rem', sm: '0.9rem'},
                ...sx
            }}
        />
    );
};

export default Label;