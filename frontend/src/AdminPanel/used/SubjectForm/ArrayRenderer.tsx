import {type FC} from 'react';
import {type ArrayRendererProps, makeFillable} from "../../../components/FormTree";
import {Flex} from "../../../components/FlexGrid.tsx";
import {Box, Button, IconButton} from "@mui/material";
import {Add as AddIcon, Delete as DeleteIcon} from "@mui/icons-material";
import OnChangedTextFieldRenderer from "./OnChangedTextFieldRenderer.tsx";

const ArrayRenderer: FC<ArrayRendererProps> = ({_vals, setVals, renderItem}) => {
    return (
        <Box>
            {_vals.map((val, index) => (
                <Flex sx={{gap: 1, mb: 2}} key={`flex${index}`}>
                    {renderItem(val, index)}

                    {index != 0 && <IconButton
                        color="error"
                        size="small"
                        onClick={index != 0 ? () => {
                            setVals(prev => {
                                return prev.filter((_, i) => i !== index);
                            })
                        } : undefined}
                    >
                        <DeleteIcon/>
                    </IconButton>}
                </Flex>
            ))}
            <Button
                startIcon={<AddIcon/>}
                variant="outlined"
                size="small"
                onClick={() => {
                    setVals((prev) => {
                        return [...prev, makeFillable(["", OnChangedTextFieldRenderer])]
                    })
                }}
            >
                Add Description
            </Button>
        </Box>
    );
};

export default ArrayRenderer;