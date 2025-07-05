import {type FC} from 'react';
import {useDifficulties} from "../../../hooks.ts";
import Filter from "../Filter.tsx";
import FilterUnit from "../FilterUnit.tsx";
import type {DifficultyFiltersProps} from "../../../types/filters/difficulty.ts";

const Difficulties: FC<DifficultyFiltersProps> = ({difficultyTypes, setFilters}) => {
    const addDifficulty = (newDifficulty: string) => {
        setFilters((prevFilters) => ({
            ...prevFilters,
            difficultyTypes: [...prevFilters.difficultyTypes, newDifficulty],
        }));
    };
    const removeDifficulty = (difficultyToRemove: string) => {
        setFilters((prevFilters) => ({
            ...prevFilters,
            difficultyTypes: prevFilters.difficultyTypes.filter((difficulty) => difficulty != difficultyToRemove)
        }));
    }
    const {data, isLoading, error} = useDifficulties()
    if (error) return <h1>error</h1>
    if (isLoading) return <h1>loading</h1>
    return (
        <Filter title="Уровень сложности">
            {data!.map((unit) => {
                return <FilterUnit
                    clicked={difficultyTypes.includes(unit.type)}
                    onClick={(clicked) => {
                        if (clicked) addDifficulty(unit.type)
                        else removeDifficulty(unit.type)
                    }} key={unit.type} unit={unit}/>
            })}
        </Filter>
    );
};

export default Difficulties;