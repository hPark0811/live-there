import React from 'react';
import styles from './NavItems.module.scss';
import {NavLink, useHistory} from "react-router-dom";

const NavItems = () => {
  const history = useHistory();

  const preventRouting = (event) => {
    if (history?.location?.pathname && history?.location?.pathname.includes('/cost-of-living')) {
      event.preventDefault();
      event.stopPropagation();
    }
  }

  return (
    <ul className={styles.NavItems}>
      <li className={styles.Item}>
        <NavLink to="/"
                 activeClassName={styles.active}
                 exact>HOME</NavLink>
      </li>
      <li className={styles.Item}>
        <NavLink to="/cost-of-living"
                 onClick={preventRouting}
                 activeClassName={styles.active}>COST OF LIVING</NavLink>
      </li>
      <li className={styles.Item}>
        <NavLink to="/about"
                 activeClassName={styles.active}
                 exact>ABOUT US</NavLink>
      </li>
      {/*<li className={styles.Item}>
      <NavLink to="/user" activeClassName={styles.active} exact>
        <UserIcon/>
      </NavLink>
    </li>*/}
    </ul>
  )
}

export default NavItems;
