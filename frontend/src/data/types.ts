import type {ReactNode} from "react";
import type {GridProps} from "@mui/material/Grid";
import type {SxProps} from "@mui/material";

export interface Difficulty {
    type: string;
    label: string;
    icon: string;
    color: string;
}

export interface Grade {
    id: number;
    grade: string
}


export interface Subject {
    type: string;
    label: string;
    icon: string;
    color: string;
    additional_description: string[];
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
    image_url?: string;
    organization?: string;
    difficulty?: string;
}

export interface ChildrenProps {
    children?: ReactNode
}

export interface PassThroughProps extends GridProps {
    sx?: SxProps;
    children?: ReactNode;
}
