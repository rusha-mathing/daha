import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import App from './App.tsx'

import './index.css'
import {HashRouter} from "react-router-dom";

const root = createRoot(
    document.getElementById('root')! as HTMLElement
);
root.render(
    <StrictMode>
        <HashRouter>
            <App/>
        </HashRouter>
    </StrictMode>
);