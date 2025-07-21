import {type FC} from "react";
import {CssBaseline, ThemeProvider} from "@mui/material";
import theme from "./theme";
import MainPage from "./MainPage";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import AdminPanel from "./AdminPanel";

const client = new QueryClient()
const App: FC = () => {
    return (
        <QueryClientProvider client={client}>
            <ThemeProvider theme={theme}>
                <CssBaseline/>
                <BrowserRouter>
                    <Routes>
                        <Route path="/" element={<MainPage/>}/>
                        <Route path="/admin" element={<AdminPanel/>}/>
                    </Routes>
                </BrowserRouter>
            </ThemeProvider>
        </QueryClientProvider>
    )
}

export default App;