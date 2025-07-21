import {type FC} from 'react';
import type {ItemRendererProps} from "../../../components/FormTree";
import {TextField} from "@mui/material";

interface LabelUserData {
    label: string;
}

const OnChangedTextFieldRenderer: FC<ItemRendererProps> = ({
                                                               _val, setVal,
                                                               userData,
                                                           }) => {
    const label = userData && typeof userData === 'object' && 'label' in userData
        ? (userData as LabelUserData).label
        : undefined;
    const type = userData && typeof userData === 'object' && 'type' in userData ? (userData as {
        type: string
    }).type : undefined
    return <TextField type={type} label={label} value={_val} onChange={(e) => setVal(e.target.value)}/>;
};

export default OnChangedTextFieldRenderer;