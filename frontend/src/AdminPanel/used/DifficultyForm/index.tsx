import {type FC} from 'react';
import {
    type FillableStringified,
    FormTreeRenderer,
    useFormTree,
    type UserDataStringified
} from "../../../components/FormTree";
import type {Subject} from "../../../types/filters/subject.ts";
import {Box, Button, Card, CardContent, Typography} from "@mui/material";
import {
    Add as AddIcon, Clear as ClearIcon, Save as SaveIcon,

} from "@mui/icons-material";
import {Flex} from "../../../components/FlexGrid.tsx";
import OnChangedTextFieldRenderer from "./OnChangedTextFieldRenderer.tsx";
import ObjectRenderer from "./ObjectRenderer.tsx";
import FileInputRenderer from "./FileInputRenderer.tsx";
import type {Difficulty} from "../../../types/filters/difficulty.ts";

const initialDifficulty: FillableStringified<Difficulty> = {
    type: "",
    label: "",
    icon: ["", FileInputRenderer],
    color: "",
}


const subjectUserData: UserDataStringified<Subject> = {
    type: {label: "Type"},
    label: {label: "Label"},
    icon: {label: "Icon"},
    color: {label: "Color", type: "color"},
};

const DifficultyForm: FC = () => {
    const {fillable, setFillable, reset, value} = useFormTree(initialDifficulty, {
        itemRenderer: OnChangedTextFieldRenderer,
        objectRenderer: ObjectRenderer,
        userData: subjectUserData
    })
    return (
        <Card sx={{height: 'fit-content'}}>
            <CardContent sx={{p: 4}}>
                <Typography variant="h6" gutterBottom
                            sx={{mb: 3, display: 'flex', alignItems: 'center', gap: 1}}>
                    <AddIcon color="primary"/>
                    Difficulty
                </Typography>

                <Flex component="form"
                      sx={{flexDirection: 'column', gap: 3}}>
                    <Flex sx={{gap: 2, flexWrap: 'wrap'}}>
                        <FormTreeRenderer value={fillable} onChange={setFillable} userData={subjectUserData}/>
                    </Flex>
                    <Box sx={{display: 'flex', gap: 2, mt: 2}}>
                        <Button
                            type="submit"
                            variant="contained"
                            startIcon={<SaveIcon/>}
                            sx={{flex: 1}}
                        >
                            Save Difficulty
                        </Button>
                        <Button
                            onClick={reset}
                            variant="outlined"
                            startIcon={<ClearIcon/>}
                        >
                            Reset
                        </Button>
                    </Box>
                </Flex>
                {JSON.stringify(value)}
            </CardContent>
        </Card>

    );
};

export default DifficultyForm;