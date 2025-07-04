import type {Difficulty, Subject, Typeable} from "../src/data/types.ts";

import {useQuery, type UseQueryResult} from "@tanstack/react-query";
import {useMemo} from 'react';
import type {Course, Grade} from "../src/data/types.ts";

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


export function useCourses() {
    return useEndpoint<Course[]>("courses");
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