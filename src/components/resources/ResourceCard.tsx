import {Card, CardContent, Typography, Button, Box, Chip, Stack, useTheme} from '@mui/material';
import {
    setupGetDifficulty,
    setupGetSubject
} from '../../data/resources.ts';
import type {Course, Difficulty, Subject} from "../../data/types.ts";
import {useEffect, useState} from "react";

interface ResourceCardProps {
    resource: Course;
}

const ResourceCard: React.FC<ResourceCardProps> = ({resource}) => {
    const theme = useTheme();
    const [getSubject, setGetSubject] = useState<(subject: string) => Subject | undefined>(() => () => undefined);
    const [getDifficulty, setGetDifficulty] = useState<(difficulty: string) => Difficulty | undefined>(() => () => undefined);

    // Fetch subject and difficulty functions using useEffect
    useEffect(() => {
        const fetchData = async () => {
            try {
                const subjectFn = await setupGetSubject();
                setGetSubject(() => subjectFn);

                const difficultyFn = await setupGetDifficulty();
                setGetDifficulty(() => difficultyFn);
            } catch (error) {
                console.error('Error fetching subject or difficulty data:', error);
            }
        };

        fetchData();
    }, []); // Empty dependency array to run once on mount

    // Format date with proper month declension and year
    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        const day = date.getDate();
        const year = date.getFullYear();

        // Months in genitive case
        const monthsGenitive = [
            'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
        ];

        const month = monthsGenitive[date.getMonth()];
        return `${day} ${month} ${year}`;
    };

    // Enhanced course descriptions (2-3 sentences)
    const getEnhancedDescription = (description: string) => {
        // If description is already long enough, use it as is
        if (description.length > 150) return description;

        // Ensure proper ending for the initial description
        let formattedDescription = description;

        // Add period if missing and description doesn't end with punctuation
        if (formattedDescription &&
            !formattedDescription.endsWith('.') &&
            !formattedDescription.endsWith('!') &&
            !formattedDescription.endsWith('?')) {
            formattedDescription += '.';
        }

        // Additional descriptions for different subjects
        if (resource.subjectTypes && resource.subjectTypes.length > 0) {
            const primarySubject = resource.subjectTypes[0];
            const additions = getSubject(primarySubject)?.additionalDescription;

            if (additions) {
                return `${formattedDescription} ${additions.join(' ')}`;
            }
        }

        // Generic additions if no subject-specific description is found
        return `${formattedDescription} Программа разработана ведущими специалистами с учетом современных требований отрасли. Участники получат актуальные знания и ценные практические навыки.`;
    };


    return (
        <Card sx={{
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            transition: 'all 0.3s ease',
            borderRadius: {xs: '6px', sm: '8px'},
            overflow: 'visible',
            backgroundColor: 'white',
            boxShadow: 'none',
            border: '1px solid #e0e0e0',
            '&:hover': {
                borderColor: theme.palette.primary.main,
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.04)',
            },
            position: 'relative',
            mb: {xs: 2, sm: 3},
            width: '100%'
        }}>
            <CardContent sx={{
                pt: {xs: 2.5, sm: 3, md: 3.5},
                pb: {xs: 1.5, sm: 2},
                flexGrow: 1,
                px: {xs: 2, sm: 2.5, md: 3},
                display: 'flex',
                flexDirection: 'column',
                gap: {xs: 1, sm: 1.5}
            }}>
                {/* Заголовок - крупным шрифтом */}
                <Typography
                    component="div"
                    variant="h5"
                    sx={{
                        fontSize: {xs: '1.2rem', sm: '1.35rem', md: '1.5rem'},
                        fontWeight: 700,
                        letterSpacing: '-0.01em',
                        lineHeight: 1.2,
                        color: '#4361ee', // Более яркий синий цвет для заголовка
                        mb: {xs: 0.3, sm: 0.5}
                    }}
                >
                    {resource.title}
                </Typography>

                {/* Организатор курса - более заметно, без "в" */}
                {resource.organizer && (
                    <Typography
                        variant="body1"
                        sx={{
                            fontWeight: 600,
                            fontSize: {xs: '1rem', sm: '1.05rem', md: '1.1rem'},
                            mb: {xs: 0.5, sm: 1},
                            color: '#616161'
                        }}
                    >
                        {resource.organizer}
                    </Typography>
                )}

                {/* Даты как аналог зарплаты */}
                <Typography
                    variant="h6"
                    sx={{
                        fontWeight: 600,
                        fontSize: {xs: '1.2rem', sm: '1.25rem', md: '1.35rem'},
                        mb: {xs: 1.5, sm: 2},
                        color: '#000',
                        letterSpacing: '-0.01em'
                    }}
                >
                    {formatDate(resource.startDate)} — {formatDate(resource.endDate)}
                </Typography>

                {/* Чипсы для классов и типа */}
                <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap sx={{mb: {xs: 1.5, sm: 2}}}>
                    {resource.grades.map((grade) => (
                        <Chip
                            key={grade}
                            label={`${grade} класс`}
                            size="medium"
                            sx={{
                                borderRadius: {xs: '4px', sm: '6px'},
                                backgroundColor: '#f5f5f5',
                                color: '#333',
                                px: {xs: 1, sm: 1.5},
                                py: {xs: 2, sm: 2.5},
                                height: 'auto',
                                mb: 1,
                                fontWeight: 500,
                                fontSize: {xs: '0.85rem', sm: '0.9rem'}
                            }}
                        />
                    ))}
                    {resource.difficultyLevel && (
                        <Chip
                            label={`Уровень: ${getDifficulty(resource.difficultyLevel)?.label}`} // TODO: ?.
                            size="medium"
                            sx={{
                                borderRadius: {xs: '4px', sm: '6px'},
                                backgroundColor: '#f0f7ff',
                                color: '#0066cc',
                                px: {xs: 1, sm: 1.5},
                                py: {xs: 2, sm: 2.5},
                                height: 'auto',
                                mb: 1,
                                fontWeight: 500,
                                fontSize: {xs: '0.85rem', sm: '0.9rem'}
                            }}
                        />
                    )}
                </Stack>

                {/* Описание с расширенным содержанием */}
                <Box sx={{mb: {xs: 2, sm: 2.5, md: 3}}}>
                    <Typography
                        variant="body1"
                        sx={{
                            lineHeight: {xs: 1.5, sm: 1.6},
                            color: '#333333',
                            fontSize: {xs: '0.95rem', sm: '1rem'}
                        }}
                    >
                        {getEnhancedDescription(resource.description)}
                    </Typography>
                </Box>

                {/* Блок с предметами (без заголовка) */}
                <Box sx={{mb: {xs: 1.5, sm: 2}}}>
                    <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap sx={{mb: 0.5}}>
                        {resource.subjectTypes.map((type) => (
                            <Chip
                                key={type}
                                label={getSubject(type)?.label}
                                size="medium"
                                sx={{
                                    mb: 0.75,
                                    fontWeight: 500,
                                    fontSize: {xs: '0.85rem', sm: '0.9rem'},
                                    backgroundColor: `${getSubject(type)?.color}10`,
                                    color: getSubject(type)?.color,
                                    height: {xs: '28px', sm: '32px'},
                                    borderRadius: {xs: '4px', sm: '6px'},
                                    px: {xs: 0.5, sm: 1},
                                    '&:hover': {
                                        backgroundColor: `${getSubject(type)?.color}20`,
                                    }
                                }}
                            />
                        ))}
                    </Stack>
                </Box>
            </CardContent>

            {/* Кнопка внизу карточки */}
            <Box sx={{
                display: 'flex',
                justifyContent: 'flex-start',
                px: {xs: 2, sm: 2.5, md: 3},
                pb: {xs: 2, sm: 2.5, md: 3},
                mt: 'auto'
            }}>
                <Button
                    variant="contained"
                    href={resource.url}
                    target="_blank"
                    rel="noopener"
                    sx={{
                        borderRadius: '4px',
                        px: {xs: 3, sm: 3.5, md: 4},
                        py: {xs: 0.75, sm: 1},
                        fontWeight: 600,
                        letterSpacing: '0.01em',
                        fontSize: {xs: '0.9rem', sm: '0.95rem'},
                        boxShadow: 'none',
                        backgroundColor: '#000',
                        color: '#fff',
                        textTransform: 'none',
                        '&:hover': {
                            backgroundColor: '#333',
                            boxShadow: 'none'
                        }
                    }}
                >
                    Ссылка на курс
                </Button>
            </Box>
        </Card>
    );
};

export default ResourceCard;
