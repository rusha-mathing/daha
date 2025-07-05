import {type FC} from 'react';
import {Drawer} from "@mui/material";
import {type ModalProps} from "@mui/material/Modal";
import type {ChildrenProps} from "../../types";

interface MobilePanelProps extends ChildrenProps {
    open?: boolean;
    onClose?: ModalProps['onClose'];
}

const MobilePanel: FC<MobilePanelProps> = ({open, onClose, children}) => {
    return (
        <Drawer
            anchor="left"
            open={open}
            onClose={onClose}
            slotProps={
                {
                    paper: {
                        sx: {
                            width: {xs: '85%', sm: 350},
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