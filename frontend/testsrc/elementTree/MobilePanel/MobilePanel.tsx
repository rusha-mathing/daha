import {type FC} from 'react';
import type {ChildrenProps} from '../../../src/data/types';
import {Drawer, type Theme, useMediaQuery} from "@mui/material";

const MobilePanel: FC<ChildrenProps> = ({children}) => {
    const isMobile = useMediaQuery((theme: Theme) => theme.breakpoints.down('md'));
    return (
        <Drawer
            anchor="left"
            open={isMobile} // TODO
            slotProps={
                {
                    paper: {
                        sx: {
                            width: {xs: '85%', sm: 350}, // Адаптивная ширина для разных экранов
                            borderRadius: '0 16px 16px 0',
                            boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                            maxWidth: '100vw'
                        }
                    }
                }
            }
        >
            {children}
        </Drawer>
    );
};

export default MobilePanel;