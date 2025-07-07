import {type FC} from 'react';
import type {ItemRendererProps} from "../../../components/FormTree";
import FileInput from "../../../components/FileInput.tsx";

const FileInputRenderer: FC<ItemRendererProps> = ({setVal}) => {
    return (
        <FileInput setFile={(val) => setVal(val)}/>
    );
};

export default FileInputRenderer;