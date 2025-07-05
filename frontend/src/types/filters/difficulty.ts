import type {Filter, SetFiltersProps} from "./index.ts";

export type Difficulty = Filter

export interface DifficultyFilters {
    difficultyTypes: string[];
}
export type DifficultyFiltersProps = SetFiltersProps & DifficultyFilters