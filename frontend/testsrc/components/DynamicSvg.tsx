import type {FC} from "react";
import {SvgIcon} from "@mui/material";
interface DynamicSvgProps {
    svg: string;
}

const DynamicSvg: FC<DynamicSvgProps> = ({svg}) => {
    const Icon = () => (
        <svg
            focusable={false}
            viewBox="0 0 24 24"
            dangerouslySetInnerHTML={{__html: svg}}
        />
    )
    return (
        <SvgIcon>
            <Icon/>
        </SvgIcon>
    )
}
export default DynamicSvg;