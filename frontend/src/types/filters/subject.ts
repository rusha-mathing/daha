import type {Filter, SetFiltersProps} from "./index.ts";

export interface Subject extends Filter {
    additional_description: string[];
}

export interface SubjectFilters {
    subjectTypes: string[];
}

export type SubjectFiltersProps = SetFiltersProps & SubjectFilters