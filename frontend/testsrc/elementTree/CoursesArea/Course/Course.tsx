import {type FC} from "react";
import {Card, CardContent, Typography, Button, Box, Stack, useTheme} from '@mui/material';
import Label from "../../../components/Label";
import {Flex} from "../../../components/FlexGrid.tsx";

const Course: FC = () => {
    const theme = useTheme()
    return (
        <Card sx={{
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            transition: 'all 0.3s ease',
            borderRadius: {xs: '6px', sm: '8px'},
            overflow: 'visible',
            backgroundColor: theme.palette.background.paper,
            boxShadow: 'none',
            border: '1px solid' +  theme.palette.grey["200"],
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
                <Typography
                    component="div"
                    variant="h6"
                    sx={{
                        fontSize: {xs: '1.2rem', sm: '1.35rem', md: '1.5rem'},
                        letterSpacing: '-0.01em',
                        lineHeight: 1.2,
                        color: theme.palette.primary.main,
                        mb: {xs: 0.3, sm: 0.5}
                    }}
                >
                    Основы машинного обучения и нейронных сетей
                </Typography>
                <Typography
                    variant="h6"
                    sx={{
                        fontSize: {xs: '1rem', sm: '1.05rem', md: '1.1rem'},
                        mb: {xs: 0.5, sm: 1},
                        color: theme.palette.grey["700"]
                    }}
                >
                    Яндекс
                </Typography>
                <Typography
                    variant="h6"
                    sx={{
                        fontSize: {xs: '1.2rem', sm: '1.25rem', md: '1.35rem'},
                        mb: {xs: 1.5, sm: 2},
                        color: theme.palette.text.primary,
                        letterSpacing: '-0.01em'
                    }}
                >
                    15 сентября 2025 — 20 января 2026
                </Typography>

                <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap sx={{mb: {xs: 1.5, sm: 2}}}>
                    <Label label='10 класс' sx={{
                        height: 'auto',
                        py: {xs: 2, sm: 2.5},
                        backgroundColor: theme.palette.grey["100"],
                        color: theme.palette.grey['800']
                    }}/>
                    <Label label='Уровень: средний' sx={{
                        height: 'auto',
                        py: {xs: 2, sm: 2.5},
                        backgroundColor: theme.palette.primary.main + "25",
                        color: theme.palette.primary.main,
                    }}/>
                </Stack>

                <Box sx={{mb: {xs: 2, sm: 2.5, md: 3}}}>
                    <Typography
                        variant="body1"
                        sx={{
                            lineHeight: {xs: 1.5, sm: 1.6},
                            color: theme.palette.grey["800"],
                            fontSize: {xs: '0.95rem', sm: '1rem'}
                        }}
                    >
                        Ведут специалисты из Яндекса с реальными кейсами из индустрии. Слушатели осваивают практические
                        навыки построения нейронных сетей и работы с большими данными. Курс включает работу с реальными
                        проектами и актуальными инструментами искусственного интеллекта.
                    </Typography>
                </Box>

                <Box sx={{mb: {xs: 1.5, sm: 2}}}>
                    <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap sx={{mb: 0.5}}>
                        <Label
                            label="Искусственный интеллект"
                            sx={{
                                mb: 0.75,
                                fontSize: {xs: '0.85rem', sm: '0.9rem'},
                                backgroundColor: theme.palette.primary.dark + "10",
                                color: theme.palette.primary.dark,
                                height: {xs: '28px', sm: '32px'},
                                px: {xs: 0.5, sm: 1}
                            }}
                        />
                    </Stack>
                </Box>
            </CardContent>
            <Flex sx={{
                justifyContent: 'flex-start',
                px: {xs: 2, sm: 2.5, md: 3},
                pb: {xs: 2, sm: 2.5, md: 3},
                mt: 'auto'
            }}>
                <Button
                    variant="contained"
                    href="https://example.com"
                    target="_blank"
                    rel="noopener"
                    sx={{
                        px: {xs: 3, sm: 3.5, md: 4},
                        py: {xs: 0.75, sm: 1},
                        fontSize: {xs: '0.9rem', sm: '0.95rem'},
                    }}
                >
                    Ссылка на курс
                </Button>
            </Flex>
        </Card>
    );
};

export default Course;
