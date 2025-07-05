import {type FC} from 'react';
import {useGrades} from "../../../hooks.ts";
import Filter from "../Filter.tsx";
import Grade from "../Grade.tsx";
import type {GradeFiltersProps} from "../../../types/filters/grade.ts";

const Grades: FC<GradeFiltersProps> = ({grades, setFilters}) => {
    const addGrade = (newGrade: number) => {
        setFilters((prevFilters) => ({
            ...prevFilters,
            grades: [...prevFilters.grades, newGrade],
        }));
    };
    const removeGrade = (gradeToRemove: number) => {
        setFilters((prevFilters) => ({
            ...prevFilters,
            grades: prevFilters.grades.filter((grade) => grade != gradeToRemove)
        }));
    }
    const {data, isLoading, error} = useGrades()
    if (error) return <h1>error</h1>
    if (isLoading) return <h1>loading</h1>
    return (
        <Filter direction="row" title="Классы">
            {data!.map((unit) => {
                return <Grade
                    clicked={grades.includes(unit.grade)}
                    onClick={(clicked) => {
                        if (clicked) addGrade(unit.grade)
                        else {
                            removeGrade(unit.grade)
                            window.scrollTo({
                                top: 0,
                                behavior: 'instant',
                            });
                        }
                    }}
                    key={"grade_" + unit.grade} grade={unit.grade}/>
            })}
        </Filter>
    );
};

export default Grades;