import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import theme from './theme/theme';
import './index.css'
import App from './App.tsx'
import {CssBaseline, ThemeProvider} from "@mui/material";
import {HashRouter} from "react-router-dom";

const root = createRoot(
    document.getElementById('root')! as HTMLElement
);
root.render(
    <StrictMode>
        <ThemeProvider theme={theme}>
            <CssBaseline/> {/* Сбрасываем стандартные стили браузера */}
            <HashRouter>
                <App/>
            </HashRouter>
        </ThemeProvider>
    </StrictMode>
);