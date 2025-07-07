import {type FC} from 'react';
import Label from "../Label.tsx";
import {useSubjectLookup} from "../../../hooks.ts";
import {Skeleton} from "@mui/material";
import {capitalize} from "../funcs.ts";

interface SubjectLabelProps {
    subject: string;
}

const UseSubjectLabel: FC<SubjectLabelProps> = ({subject}) => {
    const {lookup, isLoading, error} = useSubjectLookup()
    if (error) return <h1>error</h1>
    if (isLoading) return <Skeleton variant="rounded" width={160} height={30}/>
    if (!lookup[subject]?.label) return <></>
    return (
        <Label
            label={capitalize(lookup[subject].label)}
            sx={{
                mb: 0.75,
                fontSize: {xs: '0.85rem', sm: '0.9rem'},
                backgroundColor: lookup[subject]?.color + "10",
                color: lookup[subject]?.color,
                height: {xs: '28px', sm: '32px'},
                px: {xs: 0.5, sm: 1}
            }}
        />
    );
};

export default UseSubjectLabel;