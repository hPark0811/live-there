import React from 'react';
import styles from './NavItems.module.scss';
import {NavLink} from "react-router-dom";
import {ReactComponent as UserIcon} from '../../../assets/user.svg';

const NavItems = () => (
  <ul className={styles.NavItems}>
    <li className={styles.Item}>
      <NavLink to="/" activeClassName={styles.active} exact>HOME</NavLink>
    </li>
    <li className={styles.Item}>
      <NavLink to="/cost-of-living/overview/uwo" activeClassName={styles.active} exact>TEST</NavLink>
    </li>
    <li className={styles.Item}>
      <NavLink to="/about" activeClassName={styles.active} exact>ABOUT US</NavLink>
    </li>
    {/*<li className={styles.Item}>
      <NavLink to="/user" activeClassName={styles.active} exact>
        <UserIcon/>
      </NavLink>
    </li>*/}
  </ul>
)

export default NavItems;
