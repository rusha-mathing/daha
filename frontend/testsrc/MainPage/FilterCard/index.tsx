import {type FC} from "react";
import {Box, IconButton, type Theme, Typography, useMediaQuery, useTheme} from "@mui/material";
import {Button} from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import {Flex} from "../../components/FlexGrid.tsx";
import Filter from "./Filter.tsx";
import FilterUnit from "./FilterUnit.tsx";
import Grade from "./Grade.tsx";

interface FilterCardProps {
    onMobileCloseIconClick: () => void;
}

const FilterCard: FC<FilterCardProps> = ({onMobileCloseIconClick}) => {
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
                <Filter title="Направления">
                    <FilterUnit/>
                    <FilterUnit/>
                </Filter>
            </Box>
            <Box sx={{mt: 4}}>
                <Filter title="Уровень сложности">
                    <FilterUnit/>
                    <FilterUnit/>
                    <FilterUnit/>
                </Filter>
            </Box>
            <Box sx={{mt: 4, pb: 2}}>
                <Filter title="Классы">
                    <Grade/>
                </Filter>
            </Box>
            <Flex sx={{
                mt: 4,
                justifyContent: 'center',
                borderTop: '1px solid' + theme.palette.grey["400"],
                pt: 3
            }}>
                <Button
                    variant="outlined"
                    startIcon={<RestartAltIcon/>}
                    size="medium"
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
            </Flex>
        </Box>
    );
};

export default FilterCard;