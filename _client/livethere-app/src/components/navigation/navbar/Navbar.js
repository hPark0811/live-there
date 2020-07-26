import React from 'react';
import styles from './Navbar.module.scss';
import {ReactComponent as ToggleIcon} from '../../../assets/navToggle.svg';
import {NavLink} from "react-router-dom";
import {Desktop, Mobile} from "../../_hoc/Responsive";
import NavItems from "../navItems/NavItems";

const Navbar = (props, ref) => (
  <div className={styles.container}
       ref={ref}>
    <NavLink to='/' className={styles.logo} exact>LiveThere</NavLink>
    <Mobile>
      <ToggleIcon onClick={props.toggleSide} className={styles.toggle}/>
    </Mobile>
    <Desktop>
      <NavItems/>
    </Desktop>
  </div>
)

export default React.forwardRef(Navbar);
