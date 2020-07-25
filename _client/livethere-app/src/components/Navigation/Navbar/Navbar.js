import React from 'react';
import styles from './Navbar.module.scss';
import {ReactComponent as ToggleIcon} from '../../../assets/navToggle.svg';
import {Box} from '@material-ui/core';
import {Desktop, Mobile} from "../../_hoc/Responsive";
import NavItems from "../NavItems/NavItems";

const Navbar = () => (
  <Box display='flex'
       alignItems='center'
       className={styles.container}>
    <div className={styles.logo}>LiveThere</div>
    <Mobile>
      <ToggleIcon className={styles.toggle}/>
    </Mobile>
    <Desktop>
      <NavItems/>
    </Desktop>
  </Box>
)

export default Navbar;
