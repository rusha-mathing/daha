import {type FC} from 'react';
import Grade from './Grade/Grade';
import Filter from '../../../components/Filter';

const Grades: FC = () => {
    return (
        <Filter title='Классы'>
            <Grade/>
        </Filter>
    );
};

export default Grades;