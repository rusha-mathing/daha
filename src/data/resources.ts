import type {Difficulty, Course, Subject, Grade} from "./types.ts";

const memoizedFetch = (() => {
    const cache = new Map<string, unknown>();

    return async <T>(url: string, options: RequestInit = {}): Promise<T> => {
        const cacheKey = JSON.stringify({url, options});

        if (cache.has(cacheKey)) {
            return cache.get(cacheKey) as T;
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data: T = await response.json();
            cache.set(cacheKey, data);
            return data;
        } catch (error) {
            console.error('Fetch error:', error);
            throw error;
        }
    };
})();

const baseUrl = import.meta.env.VITE_API_URL as string;

export async function getDifficulties(): Promise<Array<Difficulty>> {
    return await memoizedFetch(`${baseUrl}/difficulties`) as Array<Difficulty>
}

export async function setupGetDifficulty(): Promise<(type: string) => Difficulty | undefined> {
    const map: Map<string, Difficulty> = new Map();
    const difficulties: Array<Difficulty> = await getDifficulties();
    for (const difficulty of difficulties) {
        map.set(difficulty.type, difficulty);
    }
    return ((type: string): Difficulty | undefined => {
        return map.get(type);
    })
}


export async function getSubjects(): Promise<Array<Subject>> {
    return await memoizedFetch(`${baseUrl}/subjects`) as Array<Subject>
}


export async function setupGetSubject(): Promise<(type: string) => Subject | undefined> {
    const map: Map<string, Subject> = new Map();
    const subjects: Array<Subject> = await getSubjects();
    for (const difficulty of subjects) {
        map.set(difficulty.type, difficulty);
    }
    return ((type: string): Subject | undefined => {
        return map.get(type);
    })
}


export async function getGrades(): Promise<Array<string>> {
    return (await memoizedFetch(`${baseUrl}/grades`) as Array<Grade>).map((d) => String(d.grade));
}


export async function getCourses(): Promise<Array<Course>> {
    return (await memoizedFetch(`${baseUrl}/courses`)) as Array<Course>
}