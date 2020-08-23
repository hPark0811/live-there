import React from "react";
import Typography from "@material-ui/core/Typography";
import styles from "./Home.module.scss";
import {connect} from "react-redux";
import UniversitySearch from "../../components/search/universitySearch/UniversitySearch";

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
        <UniversitySearch/>
      </div>
      {/* TODO: Add cards */}
    </>
  )
}

const mapStateToProps = state => {
  return {
    universityDict: state.universityDict
  }
}

export default connect(mapStateToProps)(Home);
