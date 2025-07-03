import {type FC} from "react";
import Difficulty from "./Difficulty/Difficulty.tsx";
import Filter from "../../../components/Filter.tsx";

const Difficulties: FC = () => {
    return (
        <Filter title="Уровень сложности:">
            <Difficulty/>
            <Difficulty/>
            <Difficulty/>
        </Filter>
    );
};

export default Difficulties;