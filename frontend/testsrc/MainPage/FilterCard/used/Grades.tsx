import {type FC} from 'react';
import {useGrades} from "../../../hooks.ts";
import Filter from "../Filter.tsx";
import Grade from "../Grade.tsx";

const Grades: FC = () => {
    const {data, isLoading, error} = useGrades()
    if (error) return <h1>error</h1>
    if (isLoading) return <h1>loading</h1>
    return (
        <Filter direction="row" title="Классы">
            {data!.map((unit) => <Grade key={"grade_" + unit.grade} grade={unit.grade}/>)}
        </Filter>
    );
};

export default Grades;