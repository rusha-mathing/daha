import type {SetFiltersProps} from "./index.ts";

export interface Grade {
    id: number;
    grade: number
}

export interface GradeFilters {
    grades: number[];
}
export type GradeFiltersProps = SetFiltersProps & GradeFilters