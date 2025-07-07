export interface Course {
    id?: string;
    title: string;
    description: string;
    subjects: string[];
    grades: number[];
    start_date: string;
    end_date: string;
    url: string;
    image_url: string;
    organization: string;
    difficulty: string;
}