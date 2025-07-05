import type {ReactNode} from "react";
import type {GridProps} from "@mui/material/Grid";
import type {SxProps} from "@mui/material";

export interface ChildrenProps {
    children?: ReactNode
}

export interface PassThroughProps extends GridProps {
    sx?: SxProps;
    children?: ReactNode;
}
