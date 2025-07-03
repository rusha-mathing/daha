import {type FC} from "react";
import {Box, IconButton, type Theme, Typography, useMediaQuery} from "@mui/material";
import {Button} from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import Subjects from "./Subjects/Subjects";
import Difficulties from "./Difficulties/Difficulties.tsx";
import Grades from "./Grades/Grades.tsx";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import {Flex} from "../../components/FlexGrid.tsx";

const FilterCard: FC = () => {
    const isMobile = useMediaQuery((theme: Theme) => theme.breakpoints.down('md'));
    return (
        <Box sx={{p: {xs: 2, md: 3}}}>
            {isMobile && (
                <Flex sx={{justifyContent: 'space-between', alignItems: 'center', mb: 3}}>
                    <Typography variant="h6" sx={{fontWeight: 600}}>Фильтры</Typography>
                    <IconButton
                        sx={{
                            color: "red",
                            '&:hover': {
                                color: "black",
                                backgroundColor: 'rgba(58, 123, 213, 0.04)'
                            }
                        }}
                    >
                        <CloseIcon/>
                    </IconButton>
                </Flex>
            )}
            <Box>
                <Subjects/>
            </Box>
            <Box sx={{mt: 4}}>
                <Difficulties/>
            </Box>
            <Box sx={{mt: 4, pb: 2}}>
                <Grades/>
            </Box>
            <Flex sx={{
                mt: 4,
                justifyContent: 'center',
                borderTop: `1px solid blue`,
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
                        fontWeight: 500,
                        borderWidth: '1.5px',
                        '&:hover': {
                            borderWidth: '1.5px',
                            backgroundColor: 'rgba(63, 81, 181, 0.04)'
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