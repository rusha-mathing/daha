import {type Dispatch, type FC, type SetStateAction, useState} from "react";
import {Box, IconButton, type Theme, Typography, useMediaQuery, useTheme} from "@mui/material";
import {Button} from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import {Flex} from "../../components/FlexGrid.tsx";
import Difficulties from "./used/Difficulties.tsx";
import Subjects from "./used/Subjects.tsx";
import Grades from "./used/Grades.tsx";
import type {SDGFilters} from "../../types/filters";
import {filtersIsEmpty} from "../../hooks.ts";


interface FilterCardProps {
    onMobileCloseIconClick: () => void;
    filters: SDGFilters;
    setFilters: Dispatch<SetStateAction<SDGFilters>>;
}

const FilterCard: FC<FilterCardProps> = ({onMobileCloseIconClick, filters, setFilters}) => {
    const subjectTypes = filters.subjectTypes;
    const [render, setRender] = useState(true);
    const theme = useTheme()
    const isMobile = useMediaQuery((theme: Theme) => theme.breakpoints.down('md'));
    return (
        <Box sx={{p: {xs: 2, md: 3}}}>
            {isMobile && (
                <Flex sx={{justifyContent: 'space-between', alignItems: 'center', mb: 3}}>
                    <Typography variant="h6" sx={{fontWeight: 600}}>Фильтры</Typography>
                    <IconButton
                        onClick={onMobileCloseIconClick}
                        sx={{
                            color: theme.palette.grey["600"],
                            '&:hover': {
                                color: theme.palette.primary.main,
                                backgroundColor: theme.palette.primary.main + '20'
                            }
                        }}
                    >
                        <CloseIcon/>
                    </IconButton>
                </Flex>
            )}
            <Box>
                <Subjects subjectTypes={subjectTypes} setFilters={setFilters}/>
            </Box>
            <Box sx={{mt: 4}}>
                <Difficulties difficultyTypes={filters.difficultyTypes} setFilters={setFilters}/>
            </Box>
            <Box sx={{mt: 4, pb: 2}}>
                <Grades grades={filters.grades} setFilters={setFilters}/>
            </Box>
            {!filtersIsEmpty(filters) && <Flex

                sx={{
                    mt: 4,
                    justifyContent: 'center',
                    borderTop: '1px solid' + theme.palette.grey["400"],
                    pt: 3
                }}>
                <Button
                    variant="outlined"
                    startIcon={<RestartAltIcon/>}
                    size="medium"
                    onClick={() => {
                        setFilters({
                            subjectTypes: [],
                            difficultyTypes: [],
                            grades: []
                        })
                        if (render) setRender(true)
                    }}
                    sx={{
                        borderRadius: '50px',
                        px: 2.5,
                        py: 0.75,
                        '&:hover': {
                            borderWidth: '1.5px',
                            backgroundColor: theme.palette.grey["400"] + "10"
                        }
                    }}
                >
                    Сбросить фильтры
                </Button>
            </Flex>}
        </Box>
    );
};

export default FilterCard;