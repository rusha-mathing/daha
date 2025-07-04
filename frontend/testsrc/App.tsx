import {type FC} from "react";
import {Box, CssBaseline, ThemeProvider} from "@mui/material";
import theme from "../src/theme/theme.ts";
import MainPage from "./elementTree/MainPage.tsx";
import {Flex} from "./components/FlexGrid.tsx";

const App: FC = () => {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline/>
            <Flex
                sx={{
                    flexDirection: 'column',
                    minHeight: '100vh',
                    width: '100%',
                    maxWidth: '100vw',
                    overflowX: 'hidden'
                }}
            >
                <Box sx={{flex: '1 0 auto', py: {xs: 2, sm: 3, md: 4}, width: '100%'}}>
                    <MainPage/>
                </Box>
            </Flex>
        </ThemeProvider>
    )
}

export default App;