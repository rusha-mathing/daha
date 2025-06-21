import {FormControl, FormLabel, Box, useTheme, Stack, Typography, Avatar, SvgIcon} from '@mui/material';
import {getSubjects} from "../../data/resources.ts";

interface SubjectFilterProps {
  selectedSubjects: string[];
  onChange: (subjects: string[]) => void;
}

const SubjectFilter: React.FC<SubjectFilterProps> = ({ selectedSubjects, onChange }) => {
  const theme = useTheme();
  
  const handleClick = (subject: string) => {
    if (selectedSubjects.includes(subject)) {
      onChange(selectedSubjects.filter(s => s !== subject));
    } else {
      onChange([...selectedSubjects, subject]);
    }
  };

  return (
    <FormControl component="fieldset" variant="standard" sx={{ width: '100%' }}>
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
        Направления
      </FormLabel>
      <Stack spacing={1.5}>
        {Object.values(getSubjects()).map((subject) => {
          const isSelected = selectedSubjects.includes(subject.type);
            const Icon = () => {
                return <svg
                    dangerouslySetInnerHTML={{__html: subject.icon}}
                />
            }
          return (
            <Box
              key={subject.type}
              onClick={() => handleClick(subject.type)}
              sx={{ 
                display: 'flex',
                alignItems: 'center',
                padding: '8px 12px',
                borderRadius: '12px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                backgroundColor: isSelected 
                  ? `${subject.color}10`
                  : theme.palette.grey[50],
                border: isSelected 
                  ? `1px solid ${subject.color}30`
                  : `1px solid ${theme.palette.divider}`,
                '&:hover': {
                  backgroundColor: isSelected 
                    ? `${subject.color}20`
                    : theme.palette.grey[100],
                  transform: 'translateY(-2px)',
                  boxShadow: '0 2px 6px rgba(0, 0, 0, 0.05)',
                }
              }}
            >
              <Avatar 
                sx={{ 
                  width: 32, 
                  height: 32,
                  mr: 1.5,
                  backgroundColor: isSelected 
                    ? subject.color
                    : 'rgba(0, 0, 0, 0.08)',
                  color: isSelected 
                    ? '#fff'
                    : theme.palette.text.secondary,
                }}
              >
                <SvgIcon fontSize="small">
                    <Icon/>
                </SvgIcon>
              </Avatar>
              <Typography
                sx={{
                  fontWeight: 500,
                  fontSize: '0.95rem',
                  color: isSelected 
                    ? subject.color
                    : theme.palette.text.primary,
                  flex: 1
                }}
              >
                {subject.label}
              </Typography>
              {isSelected && (
                <Box
                  sx={{
                    width: 12,
                    height: 12,
                    borderRadius: '50%',
                    backgroundColor: subject.color,
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

export default SubjectFilter;