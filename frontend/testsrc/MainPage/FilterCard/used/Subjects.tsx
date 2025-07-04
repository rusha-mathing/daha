import {type FC} from 'react';
import {useSubjects} from "../../../hooks.ts";
import Filter from "../Filter.tsx";
import FilterUnit from "../FilterUnit.tsx";

const Subjects: FC = () => {
    const {data, isLoading, error} = useSubjects()
    if (error) return <h1>error</h1>
    if (isLoading) return <h1>loading</h1>
    return (
        <Filter title="Направления">
            {data!.map((unit) => <FilterUnit key={unit.type} unit={unit}/>)}
        </Filter>
    );
};

export default Subjects;