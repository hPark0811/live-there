import React, {useEffect, useLayoutEffect, useRef, useState} from "react";
import Navbar from "../../navigation/navbar/Navbar";
import SideDrawer from "../../navigation/sideDrawer/SideDrawer";
import {Mobile} from "../../_hoc/Responsive";
import {withRouter} from "react-router-dom";

const PageLayout = (props) => {
  const [isSideDrawerOpen, setSideDrawer] = useState(false);
  const [bodyStyle, setBodyStyle] = useState({});

  let navBarRef = useRef(null);

  useEffect(() => {
    let unlisten = props.history.listen(() => {
      closeSide();
    });

    // returned function will be called on component unmount
    return () => {
      unlisten();
    }
  }, []);

  // Listens to window resize event
  useLayoutEffect(() => {
    function updateSize() {
      const navbarHeight = navBarRef.current.clientHeight;
      setBodyStyle({
        marginTop: navbarHeight + 'px',
        height: (window.innerHeight - navbarHeight) + 'px'
      });
    }

    window.addEventListener('resize', updateSize);
    updateSize();
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  const toggleSide = () => {
    setSideDrawer(!isSideDrawerOpen);
  }

  const closeSide = () => {
    setSideDrawer(false);
  }

  return (
    <>
      <Navbar toggleSide={toggleSide}
              ref={navBarRef}/>
      <Mobile>
        <SideDrawer isOpen={isSideDrawerOpen}
                    closeSide={closeSide}/>
      </Mobile>
      <main style={bodyStyle}>
        {props.children}
      </main>
    </>
  )
}

export default withRouter(PageLayout);
