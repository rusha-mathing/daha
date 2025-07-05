import {type FC} from 'react';
import {useSubjects} from "../../../hooks.ts";
import Filter from "../Filter.tsx";
import FilterUnit from "../FilterUnit.tsx";
import type {SubjectFiltersProps} from "../../../types/filters/subject.ts";


const Subjects: FC<SubjectFiltersProps> = ({subjectTypes, setFilters}) => {
    const addSubject = (newSubject: string) => {
        setFilters((prevFilters) => ({
            ...prevFilters,
            subjectTypes: [...prevFilters.subjectTypes, newSubject],
        }));
    };
    const removeSubject = (subjectToRemove: string) => {
        setFilters((prevFilters) => ({
            ...prevFilters,
            subjectTypes: prevFilters.subjectTypes.filter((subject) => subject != subjectToRemove)
        }));
    }
    const {data, isLoading, error} = useSubjects()
    if (error) return <h1>error</h1>
    if (isLoading) return <h1>loading</h1>
    return (
        <Filter title="Направления">
            {data!.map((unit) => {
                return <FilterUnit
                    clicked={subjectTypes.includes(unit.type)}
                    onClick={(clicked) => {
                        window.scrollTo({
                            top: 0,
                            behavior: 'instant',
                        });
                        if (clicked) addSubject(unit.type)
                        else removeSubject(unit.type)
                    }} key={unit.type} unit={unit}/>
            })}
        </Filter>
    );
};

export default Subjects;