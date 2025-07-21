import {type Dispatch, type FC, type SetStateAction, useState} from 'react';
import {Box, Divider, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Typography} from "@mui/material";
import SchoolIcon from "@mui/icons-material/School";
import {Flex} from "../../components/FlexGrid.tsx";
import {Link} from 'react-router-dom';
import type {PageItem} from "../../types/admintypes.ts";

interface LeftSideMenuProps {
    pageItems: PageItem[];
    setComponent: Dispatch<SetStateAction<PageItem>>;
}

const LeftSideMenu: FC<LeftSideMenuProps> = ({pageItems, setComponent}) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    return (
        <Box sx={{width: 280}}>
            <Link to="/">
                <Flex sx={{p: 2, alignItems: 'center', gap: 1, alignContent: "center"}}>
                    <SchoolIcon sx={{color: 'primary.main', fontSize: 32}}/>
                    <Typography
                        sx={{
                            transform: "translate(0, 25%)",
                        }}
                        variant="h6" fontWeight="bold" color="primary">
                        Home
                    </Typography>
                </Flex>
            </Link>
            <Divider/>
            <List sx={{pt: 1}}>
                {pageItems.map((pageItem, index) => {
                    return (
                        <ListItem
                            onClick={() => {
                                setCurrentIndex(index)
                                setComponent(pageItem)
                            }}
                            key={pageItem.label}
                            disablePadding
                        >
                            <ListItemButton
                                selected={index == currentIndex}
                                sx={{
                                    mx: 1,
                                    borderRadius: 2,
                                    '&.Mui-selected': {
                                        backgroundColor: 'primary.main',
                                        color: 'white',
                                        '&:hover': {
                                            backgroundColor: 'primary.dark',
                                        },
                                        '& .MuiListItemIcon-root': {
                                            color: 'white',
                                        },
                                    },
                                }}
                            >
                                <ListItemIcon
                                    sx={{minWidth: 40}}>
                                    {pageItem.icon}
                                </ListItemIcon>
                                <ListItemText primary={pageItem.label}/>
                            </ListItemButton>
                        </ListItem>
                    )
                })}
            </List>
        </Box>
    )
}


export default LeftSideMenu;