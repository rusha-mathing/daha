export interface Difficulty {
    type: string;
    label: string;
    icon: string;
    color: string;
}

export interface Subject {
    type: string;
    label: string;
    icon: string;
    color: string;
    additionalDescription: string[];
}

export interface Resource {
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