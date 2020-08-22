import React from 'react';
import styles from './Navbar.module.scss';
import {ReactComponent as ToggleIcon} from '../../../assets/navToggle.svg';
import {NavLink} from "react-router-dom";
import {Desktop, Mobile} from "../../_hoc/Responsive";
import NavItems from "../navItems/NavItems";
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  navbar: {
    zIndex: theme.zIndex.appBar
  },
}));

const Navbar = (props, ref) => {
  const classes = useStyles();

  return (
  <div className={[styles.container, classes.navbar].join(' ')}
       ref={ref}>
    <NavLink to='/' className={styles.logo} exact>LiveThere</NavLink>
    <Mobile>
      <ToggleIcon onClick={props.toggleSide} className={styles.toggle}/>
    </Mobile>
    <Desktop>
      <NavItems/>
    </Desktop>
  </div>
)}

export default React.forwardRef(Navbar);
