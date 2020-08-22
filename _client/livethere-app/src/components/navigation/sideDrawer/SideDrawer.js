import React from 'react';

import {Backdrop} from '@material-ui/core';
import {makeStyles} from '@material-ui/core/styles';
import styles from './SideDrawer.module.scss';
import NavItems from "../navItems/NavItems";

const useStyles = makeStyles((theme) => ({
  backdrop: {
    zIndex: theme.zIndex.drawer - 1
  },
  sideDrawer: {
    zIndex: theme.zIndex.drawer
  }
}));

const SideDrawer = (props) => {
  const classes = useStyles();

  let sideDrawerClasses = [
    styles.SideDrawer,
    props.isOpen ? styles.Open : styles.Close
  ].join(' ')

  return (
    <>
      <Backdrop className={classes.backdrop}
                open={props.isOpen}
                onClick={props.closeSide}/>
      <div className={[sideDrawerClasses, classes.sideDrawer].join(' ')}>
        <nav>
          <NavItems />
        </nav>
      </div>
    </>
  );
};

export default SideDrawer;
