import {type FC} from "react";
import {Card, CardContent, Typography, Button, Box, Stack} from '@mui/material';
import Label from "../../../components/Label";
import {Flex} from "../../../components/FlexGrid.tsx";

const Course: FC = () => {
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
                borderColor: '#3f51b5',
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
                    variant="h5"
                    sx={{
                        fontSize: {xs: '1.2rem', sm: '1.35rem', md: '1.5rem'},
                        fontWeight: 700,
                        letterSpacing: '-0.01em',
                        lineHeight: 1.2,
                        color: '#4361ee',
                        mb: {xs: 0.3, sm: 0.5}
                    }}
                >
                    Основы машинного обучения и нейронных сетей
                </Typography>
                <Typography
                    variant="body1"
                    sx={{
                        fontWeight: 600,
                        fontSize: {xs: '1rem', sm: '1.05rem', md: '1.1rem'},
                        mb: {xs: 0.5, sm: 1},
                        color: '#616161'
                    }}
                >
                    Яндекс
                </Typography>
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
                    15 сентября 2025 — 20 января 2026
                </Typography>

                <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap sx={{mb: {xs: 1.5, sm: 2}}}>
                    <Label key={10} label='10 класс' sx={{
                        height: 'auto', py: {xs: 2, sm: 2.5},
                        backgroundColor: '#f5f5f5', color: '#333'
                    }}/>
                    <Label label='Уровень: средний' sx={{
                        height: 'auto', py: {xs: 2, sm: 2.5},
                        backgroundColor: '#f0f7ff', color: '#0066cc'
                    }}/>
                </Stack>

                <Box sx={{mb: {xs: 2, sm: 2.5, md: 3}}}>
                    <Typography
                        variant="body1"
                        sx={{
                            lineHeight: {xs: 1.5, sm: 1.6},
                            color: '#333333',
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
                            key="ai"
                            label="Искусственный интеллект"
                            sx={{
                                mb: 0.75,
                                fontSize: {xs: '0.85rem', sm: '0.9rem'},
                                backgroundColor: `#3f51b510`, color: '#3f51b5',
                                height: {xs: '28px', sm: '32px'},
                                px: {xs: 0.5, sm: 1},
                                '&:hover': {
                                    backgroundColor: `#3f51b520`,
                                },
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
            </Flex>
        </Card>
    );
};

export default Course;
