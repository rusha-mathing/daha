import { useState, useEffect } from 'react';
import { Container, Paper, Box, Typography, useMediaQuery, type Theme, Drawer, IconButton, useTheme, Button } from '@mui/material';
import FilterAltIcon from '@mui/icons-material/FilterAlt';
import CloseIcon from '@mui/icons-material/Close';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import {resources} from '../../data/resources.ts';
import SubjectFilter from '../filters/SubjectFilter';
import DifficultyFilter from '../filters/DifficultyFilter';
import GradeFilter from '../filters/GradeFilter';
import ResourcesList from '../resources/ResourcesList';
import type {Resource} from "../../data/types.ts";

const MainPage: React.FC = () => {
  const theme = useTheme();
  // Состояние фильтров
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const [selectedDifficulty, setSelectedDifficulty] = useState<string[]>([]);
  const [selectedGrades, setSelectedGrades] = useState<string[]>([]);
  
  // Состояние для фильтрованных и отсортированных ресурсов
  const [filteredResources, setFilteredResources] = useState<Resource[]>(resources);
  
  // Состояние для мобильной версии
  const [mobileFiltersOpen, setMobileFiltersOpen] = useState(false);
  const isMobile = useMediaQuery((theme: Theme) => theme.breakpoints.down('md'));

  // Применение фильтров
  useEffect(() => {
    let result = [...resources];

    // Фильтрация по предметам
    if (selectedSubjects.length > 0) {
      result = result.filter(resource => 
        resource.subjectTypes.some((subject: string) => selectedSubjects.includes(subject))
      );
    }
    
    // Фильтрация по уровню сложности
    if (selectedDifficulty.length > 0) {
      result = result.filter(resource => 
        resource.difficultyLevel && selectedDifficulty.includes(resource.difficultyLevel)
      );
    }

    // Фильтрация по классам
    if (selectedGrades.length > 0) {
      result = result.filter(resource => 
        resource.grades.some((grade: string) => selectedGrades.includes(grade))
      );
    }

    setFilteredResources(result);
  }, [selectedSubjects, selectedDifficulty, selectedGrades]);

  // Обработчики изменения фильтров
  const handleSubjectsChange = (subjects: string[]) => setSelectedSubjects(subjects);
  const handleDifficultyChange = (difficulty: string[]) => setSelectedDifficulty(difficulty);
  const handleGradesChange = (grades: string[]) => setSelectedGrades(grades);
  const handleResetFilters = () => {
    setSelectedSubjects([]);
    setSelectedDifficulty([]);
    setSelectedGrades([]);
  };

  // Компонент с фильтрами
  const FiltersContent = () => {
    // Проверяем, есть ли активные фильтры
    const hasActiveFilters = selectedSubjects.length > 0 || 
                          selectedDifficulty.length > 0 ||
                          selectedGrades.length > 0;
                          
    return (
    <Box sx={{ p: { xs: 2, md: 3 } }}>
      {isMobile && (
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>Фильтры</Typography>
          <IconButton 
            onClick={() => setMobileFiltersOpen(false)}
            sx={{ 
              color: theme.palette.text.secondary,
              '&:hover': {
                color: theme.palette.primary.main,
                backgroundColor: 'rgba(58, 123, 213, 0.04)'
              }
            }}
          >
            <CloseIcon />
          </IconButton>
        </Box>
      )}
      <Box>
        <SubjectFilter selectedSubjects={selectedSubjects} onChange={handleSubjectsChange} />
      </Box>
      <Box sx={{ mt: 4 }}>
        <DifficultyFilter selectedDifficulty={selectedDifficulty} onChange={handleDifficultyChange} />
      </Box>
      <Box sx={{ mt: 4, pb: 2 }}>
        <GradeFilter selectedGrades={selectedGrades} onChange={handleGradesChange} />
      </Box>
      
      {hasActiveFilters && (
        <Box sx={{ 
          mt: 4, 
          display: 'flex', 
          justifyContent: 'center',
          borderTop: `1px solid ${theme.palette.divider}`,
          pt: 3
        }}>
          <Button 
            onClick={handleResetFilters} 
            variant="outlined" 
            startIcon={<RestartAltIcon />}
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
        </Box>
      )}
    </Box>
    );
  };

  return (
    <Container maxWidth="xl" sx={{ 
      mt: { xs: 2, sm: 3, md: 4, lg: 5 }, 
      mb: { xs: 3, sm: 4, md: 5, lg: 6 }, 
      px: { xs: 1.5, sm: 2, md: 3, lg: 4 } 
    }}>
      <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column',
        gap: { xs: 2, sm: 3, md: 4 },
        width: '100%'
      }}>
        {/* Поисковая строка удалена */}
        
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: { xs: '1fr', md: '280px 1fr', lg: '320px 1fr' },
          gap: { xs: 2, sm: 2.5, md: 3, lg: 4 },
          width: '100%',
          mx: 'auto'
        }}>
          {/* Фильтры для десктопа */}
          {!isMobile ? (
            <Paper
              elevation={0}
              sx={{
                p: 0,
                height: 'fit-content',
                borderRadius: { xs: 2, sm: 3 },
                border: `1px solid ${theme.palette.divider}`,
                overflow: 'hidden',
                position: 'sticky',
                top: '20px',
                alignSelf: 'start'
              }}
            >
              <FiltersContent />
            </Paper>
          ) : (
            // Кнопка фильтров для мобильной версии
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 1 }}>
              <IconButton 
                color="primary"
                onClick={() => setMobileFiltersOpen(true)}
                sx={{ 
                  border: `1px solid ${theme.palette.divider}`,
                  borderRadius: 2,
                  boxShadow: '0 2px 4px rgba(0,0,0,0.04)'
                }}
              >
                <FilterAltIcon />
              </IconButton>
            </Box>
          )}
          
          {/* Список ресурсов */}
          <Box 
            sx={{ 
              gridColumn: { xs: '1', md: '2' },
              minHeight: { xs: '50vh', sm: '60vh' },
              width: '100%',
              overflow: 'visible'
            }}
          >
            <ResourcesList 
              resources={filteredResources}
            />
          </Box>
        </Box>
      </Box>

      {/* Выдвижная панель с фильтрами для мобильной версии */}
      <Drawer
        anchor="left"
        open={isMobile && mobileFiltersOpen}
        onClose={() => setMobileFiltersOpen(false)}
        PaperProps={{
          sx: {
            width: { xs: '85%', sm: 350 }, // Адаптивная ширина для разных экранов
            borderRadius: '0 16px 16px 0',
            boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
            maxWidth: '100vw'
          }
        }}
      >
        <FiltersContent />
      </Drawer>
    </Container>
  );
};

export default MainPage;