import {FormControl, FormLabel, Box, useTheme, Stack, Typography, SvgIcon} from '@mui/material';
import {DifficultyLevel} from '../../types';
import {difficultyColors, difficultyIcons, difficultyLabelsDifficulty} from "../../data/Resources.ts";

interface DifficultyFilterProps {
    selectedDifficulty: string[];
    onChange: (difficulty: string[]) => void;
}

const DifficultyFilter: React.FC<DifficultyFilterProps> = ({selectedDifficulty, onChange}) => {
    const theme = useTheme();

    const handleClick = (difficulty: string) => {
        if (selectedDifficulty.includes(difficulty)) {
            onChange(selectedDifficulty.filter(d => d !== difficulty));
        } else {
            onChange([...selectedDifficulty, difficulty]);
        }
    };

    return (
        <FormControl component="fieldset" variant="standard" sx={{width: '100%'}}>
            <FormLabel
                component="legend"
                sx={{
                    fontWeight: 600,
                    fontSize: '1rem',
                    color: theme.palette.text.primary,
                    mb: 1.5,
                    '&.Mui-focused': {
                        color: theme.palette.text.primary
                    }
                }}
            >
                Уровень сложности
            </FormLabel>
            <Stack spacing={1.5}>
                {Object.values(DifficultyLevel).map((difficulty) => {
                    const isSelected = selectedDifficulty.includes(difficulty);
                    const Icon = () => {
                        return <svg
                            focusable={false}
                            viewBox="0 0 24 24"
                            dangerouslySetInnerHTML={{__html: difficultyIcons[difficulty]}}
                        />
                    }
                    return (
                        <Box
                            key={difficulty}
                            onClick={() => handleClick(difficulty)}
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                padding: '8px 12px',
                                borderRadius: '12px',
                                cursor: 'pointer',
                                transition: 'all 0.2s ease',
                                backgroundColor: isSelected
                                    ? `${difficultyColors[difficulty]}10`
                                    : theme.palette.grey[50],
                                border: isSelected
                                    ? `1px solid ${difficultyColors[difficulty]}30`
                                    : `1px solid ${theme.palette.divider}`,
                                '&:hover': {
                                    backgroundColor: isSelected
                                        ? `${difficultyColors[difficulty]}20`
                                        : theme.palette.grey[100],
                                    transform: 'translateY(-2px)',
                                    boxShadow: '0 2px 6px rgba(0, 0, 0, 0.05)',
                                }
                            }}
                        >
                            <Box
                                sx={{
                                    width: 32,
                                    height: 32,
                                    mr: 1.5,
                                    borderRadius: '50%',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    backgroundColor: isSelected
                                        ? difficultyColors[difficulty]
                                        : 'rgba(0, 0, 0, 0.08)',
                                    color: isSelected
                                        ? '#fff'
                                        : theme.palette.text.secondary,
                                }}
                            >
                                <SvgIcon
                                    fontSize="small">
                                    <Icon/>
                                </SvgIcon>
                            </Box>
                            <Typography
                                sx={{
                                    fontWeight: 500,
                                    fontSize: '0.95rem',
                                    color: isSelected
                                        ? difficultyColors[difficulty]
                                        : theme.palette.text.primary,
                                    flex: 1
                                }}
                            >
                                {difficultyLabelsDifficulty[difficulty]}
                            </Typography>
                            {isSelected && (
                                <Box
                                    sx={{
                                        width: 12,
                                        height: 12,
                                        borderRadius: '50%',
                                        backgroundColor: difficultyColors[difficulty],
                                        ml: 1
                                    }}
                                />
                            )}
                        </Box>
                    );
                })}
            </Stack>
        </FormControl>
    );
};

export default DifficultyFilter;
