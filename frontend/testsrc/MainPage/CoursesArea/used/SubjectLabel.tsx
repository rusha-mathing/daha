import {type FC} from 'react';
import Label from "../Label.tsx";
import {useSubjectLookup} from "../../../hooks.ts";
import {Skeleton, useTheme} from "@mui/material";

interface SubjectLabelProps {
    subject: string;
}

const SubjectLabel: FC<SubjectLabelProps> = ({subject}) => {
    const {lookup, isLoading, error} = useSubjectLookup()
    const theme = useTheme();
    if (error) return <h1>error</h1>
    if (isLoading) return <Skeleton variant="rounded" width={160} height={30}/>
    return (
        <Label
            label={lookup[subject].label}
            sx={{
                mb: 0.75,
                fontSize: {xs: '0.85rem', sm: '0.9rem'},
                backgroundColor: theme.palette.primary.dark + "10",
                color: theme.palette.primary.dark,
                height: {xs: '28px', sm: '32px'},
                px: {xs: 0.5, sm: 1}
            }}
        />
    );
};

export default SubjectLabel;