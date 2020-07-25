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
      <NavLink to="/contact" activeClassName={styles.active} exact>CONTACT</NavLink>
    </li>
    <li className={styles.Item}>
      <NavLink to="/user" activeClassName={styles.active} exact>
        <UserIcon/>
      </NavLink>
    </li>
  </ul>
)

export default NavItems;
