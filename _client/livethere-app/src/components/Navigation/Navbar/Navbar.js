import React from 'react';
import styles from './Navbar.module.scss';
import {ReactComponent as ToggleIcon} from '../../../assets/navToggle.svg';
import {Box} from '@material-ui/core';
import {NavLink} from "react-router-dom";
import {Desktop, Mobile} from "../../_hoc/Responsive";
import NavItems from "../NavItems/NavItems";

const Navbar = (props) => (
  <Box display='flex'
       alignItems='center'
       className={styles.container}>
    <NavLink to='/' className={styles.logo} exact>LiveThere</NavLink>
    <Mobile>
      <ToggleIcon onClick={props.toggleSide} className={styles.toggle}/>
    </Mobile>
    <Desktop>
      <NavItems/>
    </Desktop>
  </Box>
)

export default Navbar;
