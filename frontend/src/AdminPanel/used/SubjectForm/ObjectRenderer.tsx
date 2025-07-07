import {type FC} from 'react';
import type {ObjectRendererProps} from "../../../components/FormTree";

const ObjectRenderer: FC<ObjectRendererProps> = ({_fields, renderField}) => {
    return (
        <div>
            {Object.entries(_fields).map(([key, field]) => (
                <div key={key}>
                    {renderField(key, field)}
                </div>
            ))}
        </div>
    );
};

export default ObjectRenderer;