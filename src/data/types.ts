export interface Difficulty {
    type: string;
    label: string;
    icon: string;
    color: string;
}

export interface Grade{
    id: number;
    grade: string
}

export interface CourseResponse {
    id: number;
    title: string;
    description: string;
    subject: string[];
    grades: number[];
    start: string;
    end: string;
    url: string;
    organization: string;
    difficulty: string;
}

export interface Subject {
    type: string;
    label: string;
    icon: string;
    color: string;
    additionalDescription: string[];
}

export interface Course {
    id: string;
    title: string;
    description: string;
    subjectTypes: string[];
    grades: string[];
    startDate: string;
    endDate: string;
    url: string;
    imageUrl?: string;
    organizer?: string;
    difficultyLevel?: string;
}