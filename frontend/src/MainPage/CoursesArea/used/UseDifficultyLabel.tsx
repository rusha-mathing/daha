import {type FC} from 'react';
import {useDifficultyLookup} from "../../../hooks.ts";
import Label from "../Label.tsx";
import {useTheme, Skeleton} from "@mui/material";

interface DifficultyLabelProps {
    difficulty: string;
}

const UseDifficultyLabel: FC<DifficultyLabelProps> = ({difficulty}) => {
    const theme = useTheme()
    const {lookup, isLoading, error} = useDifficultyLookup();
    if (error) return <h1>error</h1>
    if (isLoading) return (
        <Skeleton variant="rounded"
                  width={160}
                  sx={{backgroundColor: theme.palette.primary.main + "10"}}
                  height={60}/> // TODO: 60?
    )
    const label = lookup[difficulty]?.label
    if (!label) return <></>
    return (
        <Label
            label={"Уровень: " + label}
            sx={{
                height: 'auto',
                py: {xs: 2, sm: 2.5},
                backgroundColor: theme.palette.primary.light + "10",
                color: theme.palette.primary.light,
            }}/>
    );
};

export default UseDifficultyLabel;