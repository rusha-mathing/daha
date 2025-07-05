import {useQuery, type UseQueryResult} from "@tanstack/react-query";
import {useMemo} from 'react';
import type {SDGFilters, Typeable} from "./types/filters";
import type {Subject} from "./types/filters/subject.ts";
import type {Course} from "./types/course.ts";
import type {Difficulty} from "./types/filters/difficulty.ts";
import type {Grade} from "./types/filters/grade.ts";

const baseUrl = import.meta.env.VITE_API_URL as string;

function useEndpoint<T>(endpoint: string) {
    return useQuery({
        queryKey: [endpoint],
        queryFn: async () => {
            return (await (await fetch(`${baseUrl}/${endpoint}`)).json()) as T;
        },
        staleTime: 5 * 60 * 1000
    });
}


function useLookup<T extends Typeable>(endpointHook: () => UseQueryResult<T[], Error>) {
    const {data, isLoading, error} = endpointHook();
    const lookup = useMemo(() => {
        if (!data) return {};
        return data.reduce((map, item) => {
            map[item.type] = item;
            return map;
        }, {} as Record<string, T>)
    }, [data])
    return {lookup, isLoading, error};
}

export function useSubjects() {
    return useEndpoint<Subject[]>("subjects");
}

export function filtersIsEmpty(filters: SDGFilters) {
    return filters.subjectTypes.length === 0 &&
        filters.grades.length === 0 &&
        filters.difficultyTypes.length === 0
}

export function useCourses(filters: SDGFilters) {
    const queryResult = useEndpoint<Course[]>('courses');
    const {data, ...rest} = queryResult;
    const filteredCourses = useMemo(() => {
        if (!data) return undefined;
        let result = [...data];
        if (filters.subjectTypes.length > 0) {
            result = result.filter(resource =>
                resource.subjects.some((subject: string) => filters.subjectTypes.includes(subject))
            );
        }

        if (filters.difficultyTypes.length > 0) {
            result = result.filter(resource =>
                resource.difficulty && filters.difficultyTypes.includes(resource.difficulty)
            );
        }

        if (filters.grades.length > 0) {
            result = result.filter(resource =>
                resource.grades.some((grade: number) => filters.grades.includes(grade))
            );
        }
        return result
    }, [data, filters]);

    return {
        ...rest,
        data: filteredCourses,
    };
}

export function useDifficulties() {
    return useEndpoint<Difficulty[]>("difficulties");
}

export function useGrades() {
    return useEndpoint<Grade[]>("grades");
}


export function useSubjectLookup() {
    return useLookup(useSubjects);
}

export function useDifficultyLookup() {
    return useLookup(useDifficulties);
}