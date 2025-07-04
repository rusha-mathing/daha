import {type FC} from 'react';
import {useDifficulties} from "../../../hooks.ts";
import Filter from "../Filter.tsx";
import FilterUnit from "../FilterUnit.tsx";

const Difficulties: FC = () => {
    const {data, isLoading, error} = useDifficulties()
    if (error) return <h1>error</h1>
    if (isLoading) return <h1>loading</h1>
    return (
        <Filter title="Уровень сложности">
            {data!.map((unit) => <FilterUnit key={unit.type} unit={unit}/>)}
        </Filter>
    );
};

export default Difficulties;