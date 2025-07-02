import {FormControl, FormLabel, Box, useTheme, Stack, Typography, SvgIcon} from '@mui/material';

interface FilterInterface {
    type: string;
    label: string;
    icon?: string;
    color?: string; // Optional for cases like grades where color might not be needed
}

interface FilterProps {
    selected: string[];
    onChange: (items: string[]) => void;
    provider: () => FilterInterface[];
    title: string;
    fontWeight: string | number;
    direction?: "row" | "column" | "row-reverse" | "column-reverse";
    rounded?: boolean;
}

const Filter: React.FC<FilterProps> = ({
                                           selected,
                                           onChange,
                                           provider,
                                           title,
                                           fontWeight,
                                           direction = "column",
                                           rounded = false,
                                       }) => {
    const theme = useTheme();

    const handleClick = (item: string) => {
        if (selected.includes(item)) {
            onChange(selected.filter(d => d !== item));
        } else {
            onChange([...selected, item]);
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
                {title}
            </FormLabel>
            <Stack
                direction={direction}
                spacing={1.5}
                sx={{
                    flexWrap: direction === 'row' ? 'nowrap' : 'wrap',
                    justifyContent: direction === 'row' ? 'space-between' : 'flex-start'
                }}
            >
                {provider().map((item: FilterInterface) => {
                    const isSelected = selected.includes(item.type);
                    const Icon = () => (
                        <svg
                            focusable={false}
                            viewBox="0 0 24 24"
                            dangerouslySetInnerHTML={{__html: item.icon!}}
                        />
                    );
                    return (
                        <Box
                            key={item.type}
                            onClick={() => handleClick(item.type)}
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: rounded ? 'center' : 'flex-start',
                                padding: rounded ? 0 : '8px 12px',
                                borderRadius: rounded ? '50%' : '12px',
                                cursor: 'pointer',
                                transition: 'all 0.2s ease',
                                width: rounded ? '34px' : undefined,
                                height: rounded ? '34px' : undefined,
                                flexShrink: 0,
                                backgroundColor: isSelected
                                    ? (item.color ? `${item.color}10` : theme.palette.primary.main)
                                    : theme.palette.grey[50],
                                color: isSelected
                                    ? (item.color ? item.color : '#fff')
                                    : theme.palette.text.primary,
                                border: isSelected
                                    ? (item.color ? `1px solid ${item.color}30` : `1px solid ${theme.palette.primary.main}`)
                                    : `1px solid ${theme.palette.divider}`,
                                '&:hover': {
                                    backgroundColor: isSelected
                                        ? (item.color ? `${item.color}20` : theme.palette.primary.dark)
                                        : theme.palette.grey[100],
                                    transform: 'translateY(-2px)',
                                    boxShadow: '0 2px 6px rgba(0, 0, 0, 0.05)',
                                }
                            }}
                        >
                            {item.icon && !rounded ? (
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
                                            ? item.color
                                            : 'rgba(0, 0, 0, 0.08)',
                                        color: isSelected
                                            ? '#fff'
                                            : theme.palette.text.secondary,
                                    }}
                                >
                                    <SvgIcon fontSize="small">
                                        <Icon/>
                                    </SvgIcon>
                                </Box>
                            ) : null}

                            <Typography
                                sx={{
                                    fontWeight: fontWeight,
                                    fontSize: '0.95rem',
                                    color: isSelected
                                        ? (rounded ? '#fff' : item.color || theme.palette.text.primary)
                                        : theme.palette.text.primary,
                                    flex: rounded ? undefined : 1,
                                    textAlign: rounded ? 'center' : 'left'
                                }}
                            >
                                {item.label.charAt(0).toUpperCase() + item.label.slice(1)}
                            </Typography>
                            {!rounded && isSelected && item.color && (
                                <Box
                                    sx={{
                                        width: 12,
                                        height: 12,
                                        borderRadius: '50%',
                                        backgroundColor: item.color,
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

export default Filter;