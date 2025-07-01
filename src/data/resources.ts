import type {Difficulty, Course, Subject, Grade} from "./types.ts";


const baseUrl = import.meta.env.VITE_API_URL as string;

async function getArray<T>(endpoint: string): Promise<Array<T>> {
    return (await (await fetch(`${baseUrl}/${endpoint}`)).json()) as Array<T>
}

interface Typeable {
    type: string;
}

async function setupMap<T extends Typeable>(provider: () => Promise<Array<T>>): Promise<(type: string) => T | undefined> {
    const map: Map<string, T> = new Map();
    const items: Array<T> = await provider();
    for (const item of items) {
        map.set(item.type, item);
    }
    return ((type: string): T | undefined => {
        return map.get(type);
    })
}

export async function getDifficulties(): Promise<Array<Difficulty>> {
    return await getArray('difficulties');
}

export async function setupGetDifficulty(): Promise<(type: string) => Difficulty | undefined> {
    return await setupMap(getDifficulties);
}

export async function getSubjects(): Promise<Array<Subject>> {
    return await getArray('subjects');
}


export async function setupGetSubject(): Promise<(type: string) => Subject | undefined> {
    return await setupMap(getSubjects);
}


export async function getGrades(): Promise<Array<string>> {
    return (await getArray<Grade>('grades')).map((d: Grade) => String(d.grade));
}


export async function getCourses(): Promise<Array<Course>> {
    return await getArray('courses');
}