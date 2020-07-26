import * as React from "react";
import Typography from "@material-ui/core/Typography";
import styles from "./Home.module.scss";
import Search from "../../components/search/searchBar";

/*TODO: Remove from container*/
const Home = () => {
  return (
    <>
      <div className={styles.mainContainer}>
        <div className={styles.descriptionWrapper}>
          <Typography variant="h1"
                      component="h1">
            Explore Your University Area!
          </Typography>
          <Typography variant="subtitle1"
                      component="p">
            LiveThere provides regional research tools based on postgraduate institutions. Get an esimate of living
            cost, utility costs, and more.
          </Typography>
        </div>
        <Search/>
      </div>
      {/* TODO: Add cards */}
    </>
  )
}

export default Home;
