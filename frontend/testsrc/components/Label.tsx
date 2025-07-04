import {type FC} from 'react';
import {Chip, type SxProps, useTheme} from "@mui/material";

interface LabelProps {
    label: string;
    sx: SxProps;
}

const Label: FC<LabelProps> = ({
                                   label,
                                   sx
                               }) => {
    const theme = useTheme()
    return (
        <Chip
            label={label}
            size="medium"
            sx={{
                mb: 1,
                px: {xs: 1, sm: 1.5},
                fontWeight: theme.typography.h6.fontWeight,
                fontSize: theme.typography.subtitle2.fontSize,
                ...sx
            }}
        />
    );
};

export default Label;