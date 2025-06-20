import { TextField, InputAdornment, Paper, useTheme, IconButton, Box } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';

interface SearchBarProps {
  searchQuery: string;
  onSearchChange: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ searchQuery, onSearchChange }) => {
  const theme = useTheme();
  
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onSearchChange(event.target.value);
  };

  const handleClear = () => {
    onSearchChange('');
  };

  return (
    <Paper 
      elevation={0}
      sx={{ 
        display: 'flex',
        borderRadius: '16px',
        border: `1px solid ${theme.palette.divider}`,
        overflow: 'hidden',
        transition: 'all 0.3s ease',
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        backdropFilter: 'blur(10px)',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.03)',
        '&:hover': {
          boxShadow: '0 8px 25px rgba(0, 0, 0, 0.08)',
          borderColor: theme.palette.primary.light,
          transform: 'translateY(-2px)'
        },
        '&:focus-within': {
          borderColor: theme.palette.primary.main,
          boxShadow: `0 0 0 3px ${theme.palette.primary.main}25`
        }
      }}
    >
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Найди своё новое увлечение в мире науки и технологий..."
        value={searchQuery}
        onChange={handleChange}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Box sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                backgroundColor: theme.palette.primary.main,
                borderRadius: '50%',
                width: 32,
                height: 32,
                ml: 0.5
              }}>
                <SearchIcon sx={{ 
                  color: '#fff',
                  fontSize: '1.2rem'
                }} />
              </Box>
            </InputAdornment>
          ),
          endAdornment: searchQuery && (
            <InputAdornment position="end">
              <IconButton 
                size="small" 
                onClick={handleClear}
                sx={{
                  color: theme.palette.text.secondary,
                  '&:hover': {
                    backgroundColor: 'rgba(0, 0, 0, 0.04)'
                  }
                }}
              >
                <ClearIcon fontSize="small" />
              </IconButton>
            </InputAdornment>
          ),
          sx: {
            fieldset: { 
              border: 'none'
            },
            fontSize: '1rem',
            fontWeight: 400,
            pl: 1,
            pr: 0.5,
            py: 1,
            '& input::placeholder': {
              opacity: 0.7,
              fontStyle: 'italic'
            }
          }
        }}
      />
    </Paper>
  );
};

export default SearchBar;