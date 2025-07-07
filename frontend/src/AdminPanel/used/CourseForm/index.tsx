import {type FC} from 'react';
import type {Course} from "../../../types/course.ts";
import type {FillableStringified, UserDataStringified} from "../../../components/FormTree";

const initialCourse: FillableStringified<Course> = {
    description: "",
    difficulty: "",
    end_date: "",
    grades: [""],
    image_url: "",
    organization: "",
    start_date: "",
    subjects: [""],
    title: "",
    url: "",
}
const courseUserData: UserDataStringified<Course> = {
    description: {},
    difficulty: {},
    end_date: {},
    grades: [{}],
    image_url: {},
    organization: {},
    start_date: {},
    subjects: [{}],
    title: {},
    url: {},
}
const CourseForm: FC = () => {

    return (
        <>{initialCourse}{courseUserData}</>
    );
};

export default CourseForm;