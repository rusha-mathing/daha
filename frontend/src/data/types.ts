import type {ReactNode} from "react";
import type {GridProps} from "@mui/material/Grid";
import type {SxProps} from "@mui/material";

export interface Typeable {
    type: string;
}

export interface Filter extends Typeable {
    label: string;
    icon: string;
    color: string;
}

export type Difficulty = Filter


export interface Subject extends Filter {
    additional_description: string[];
}

export interface Grade {
    id: number;
    grade: string
}


export interface Course {
    id: string;
    title: string;
    description: string;
    subjects: string[];
    grades: number[];
    start_date: string;
    end_date: string;
    url: string;
    image_url: string;
    organization: string;
    difficulty: string;
}

export interface ChildrenProps {
    children?: ReactNode
}

export interface PassThroughProps extends GridProps {
    sx?: SxProps;
    children?: ReactNode;
}
