import type {SubjectFilters} from "./subject.ts";
import type {DifficultyFilters} from "./difficulty.ts";
import type {GradeFilters} from "./grade.ts";
import type {Dispatch, SetStateAction} from "react";

export interface Typeable {
    type: string;
}

export interface Filter extends Typeable {
    label: string;
    icon: string;
    color: string;
}

export interface SetFiltersProps {
    setFilters: Dispatch<SetStateAction<SDGFilters>>;
}

export type SDFilters = SubjectFilters & DifficultyFilters

export type SDGFilters = SDFilters & GradeFilters
