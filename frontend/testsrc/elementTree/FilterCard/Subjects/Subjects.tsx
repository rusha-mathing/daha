import {type FC} from "react";
import Filter from "../../../components/Filter.tsx";
import Subject from "./Subject/Subject.tsx";

const Subjects: FC = () => {
    return (
        <Filter title="Уровень сложности:">
            <Subject/>
            <Subject/>
            <Subject/>
            <Subject/>
            <Subject/>
            <Subject/>
            <Subject/>
        </Filter>
    );
};

export default Subjects;