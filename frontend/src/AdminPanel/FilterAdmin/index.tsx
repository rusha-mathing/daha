import {type Dispatch, type FC, type SetStateAction} from 'react';
import {
    Button,
    Box,
    Card,
    CardContent,
    Typography,
    IconButton,
    Divider, TextField
} from '@mui/material';
import {
    Add as AddIcon,
    Delete as DeleteIcon,
    ColorLens as ColorLensIcon,
    Save as SaveIcon,
    Clear as ClearIcon
} from '@mui/icons-material';
import {Flex} from '../../components/FlexGrid.tsx';
import OnChangedTextField from "./OnChangedTextField.tsx";
import FileInput from "../../components/FileInput.tsx";

interface AdditionalDescriptionInterface {
    val: string[];
    callback: Dispatch<SetStateAction<string[]>>;
}

interface FilterAdminProps {
    title?: string;
    typeCallback?: Dispatch<SetStateAction<string>>;
    labelCallback?: Dispatch<SetStateAction<string>>;
    iconCallback?: Dispatch<SetStateAction<string>>;
    colorCallback?: Dispatch<SetStateAction<string>>;
    additionalDescription?: AdditionalDescriptionInterface;
}

const FilterAdmin: FC<FilterAdminProps> = ({
                                               title,
                                               typeCallback,
                                               labelCallback,
                                               iconCallback,
                                               colorCallback,
                                               additionalDescription,
                                           }) => {
    if (!([typeCallback, labelCallback, iconCallback, colorCallback].some(r => r))) return <></>
    return (
        <Card sx={{height: 'fit-content'}}>
            <CardContent sx={{p: 4}}>
                <Typography variant="h6" gutterBottom
                            sx={{mb: 3, display: 'flex', alignItems: 'center', gap: 1}}>
                    <AddIcon color="primary"/>
                    {title}
                </Typography>

                <Flex component="form"
                      sx={{flexDirection: 'column', gap: 3}}>
                    <Flex sx={{gap: 2, flexWrap: 'wrap'}}>
                        {typeCallback &&
                            <Flex>
                                <OnChangedTextField
                                    name="type"
                                    label="Subject type"
                                    placeholder="placeholder"
                                    onChange={(event) => typeCallback(event.target.value)}
                                />
                            </Flex>}
                        {labelCallback &&
                            <Flex>
                                <OnChangedTextField
                                    name="label"
                                    label="Display Label"
                                    onChange={(event) => labelCallback(event.target.value)}
                                    placeholder="e.g., Math, Physics"
                                />
                            </Flex>}
                        {iconCallback &&
                            <Flex>
                                <FileInput setFile={iconCallback}/>
                            </Flex>
                        }
                        {colorCallback &&
                            <Flex>
                                <OnChangedTextField
                                    name="color"
                                    label="Color"
                                    type="color"
                                    fullWidth
                                    sx={{minWidth: "80px"}}
                                    onChange={(e) => colorCallback(e.target.value)}
                                    slotProps={{
                                        input: {
                                            startAdornment: (
                                                <ColorLensIcon
                                                    sx={{
                                                        mr: 1,
                                                        color: 'text.secondary'
                                                    }}/>
                                            ),
                                        }
                                    }}
                                />
                            </Flex>}
                        <Divider sx={{my: 2}}/>
                        <Flex sx={{flexDirection: "column"}}>
                            <Typography variant="subtitle1" gutterBottom>
                                Additional Descriptions
                            </Typography>
                            {additionalDescription && additionalDescription.val.map((desc, index) =>
                                <Box key={index}>
                                    <Flex sx={{gap: 1, mb: 2}}>
                                        <TextField
                                            fullWidth
                                            placeholder="Enter additional description"
                                            value={desc}
                                            size="small"
                                            onChange={(e) => {
                                                additionalDescription!.callback((prev) => {
                                                    return prev.map((el, i) => {
                                                        if (i == index) return e.target.value;
                                                        return el
                                                    })
                                                })
                                            }}
                                        />

                                        <IconButton
                                            color="error"
                                            size="small"
                                            onClick={index != 0 ? () => {
                                                additionalDescription!.callback(prev => {
                                                    return prev.filter((_, i) => i !== index);
                                                })
                                            } : undefined}
                                        >
                                            <DeleteIcon/>
                                        </IconButton>
                                    </Flex>
                                </Box>)}
                            <Button
                                startIcon={<AddIcon/>}
                                variant="outlined"
                                size="small"
                                onClick={() => {
                                    additionalDescription!.callback((prev) => {
                                        return [...prev, " "]
                                    })
                                }}
                            >
                                Add Description
                            </Button>
                        </Flex>
                    </Flex>
                    <Box sx={{display: 'flex', gap: 2, mt: 2}}>
                        <Button
                            type="submit"
                            variant="contained"
                            startIcon={<SaveIcon/>}
                            sx={{flex: 1}}
                        >
                            Save Subject
                        </Button>
                        <Button
                            variant="outlined"
                            startIcon={<ClearIcon/>}
                        >
                            Reset
                        </Button>
                    </Box>
                </Flex>
            </CardContent>
        </Card>
    );
};

export default FilterAdmin;