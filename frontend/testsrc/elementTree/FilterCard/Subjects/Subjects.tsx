import {type FC} from "react";
import Filter from "../../../components/Filter.tsx";
import Difficulty from "../Difficulties/Difficulty/Difficulty.tsx"

const Subjects: FC = () => {
    return (
        <Filter title="Направления">
            <Difficulty/>
            <Difficulty/>
            <Difficulty/>
            <Difficulty/>
            <Difficulty/>
            <Difficulty/>
            <Difficulty/>
        </Filter>
    );
};

export default Subjects;