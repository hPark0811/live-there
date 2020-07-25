import React, {useEffect, useState} from "react";
import Navbar from "../Navigation/Navbar/Navbar";
import SideDrawer from "../Navigation/SideDrawer/SideDrawer";
import {Mobile} from "../_hoc/Responsive";
import {withRouter} from "react-router-dom";

const Layout = (props) => {
  const [isSideDrawerOpen, setSideDrawer] = useState(false);

  useEffect(() => {
    let unlisten = props.history.listen(() => {
      closeSide();
    });

    // returned function will be called on component unmount
    return () => {
      unlisten();
    }
  }, [])

  const toggleSide = () => {
    setSideDrawer(!isSideDrawerOpen);
  }

  const closeSide = () => {
    setSideDrawer(false);
  }

  return (
    <>
      <Navbar toggleSide={toggleSide}/>
      <Mobile>
        <SideDrawer isOpen={isSideDrawerOpen}
                    closeSide={closeSide}/>
      </Mobile>
    </>
  )
}

export default withRouter(Layout);
