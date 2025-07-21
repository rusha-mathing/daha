import {type FC} from 'react';
import {Avatar, Box, ButtonBase, Card, CardContent, Grid, Typography} from "@mui/material";
import SchoolIcon from "@mui/icons-material/School";

const StatItem: FC = () => {
    return (
        <Grid sx={{xs: 12, sm: 6, md: 3}}>
            <ButtonBase
                sx={{width: '100%', borderRadius: 3, display: 'block'}}>
                <Card
                    sx={{
                        height: '100%',
                        background: `linear-gradient(135deg, #ff000015 0%, #ff000005 100%)`,
                        border: `1px solid #ff000020`,
                        width: '100%',
                        borderRadius: 3
                    }}
                >
                    <CardContent>
                        <Box sx={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            gap: 5,
                        }}>
                            <Box>
                                <Typography variant="h4" fontWeight="bold"
                                            color="text.primary">
                                    text
                                </Typography>
                                <Typography variant="body2" color="text.secondary"
                                            sx={{mt: 0.5}}>
                                    title
                                </Typography>
                            </Box>
                            <Avatar
                                sx={{
                                    bgcolor: "white",
                                    width: 48,
                                    height: 48,
                                }}
                            >
                                <SchoolIcon/>
                            </Avatar>
                        </Box>
                    </CardContent>
                </Card>
            </ButtonBase>
        </Grid>
    );
};

export default StatItem;