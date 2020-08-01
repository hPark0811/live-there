import React, {useEffect} from "react";
import SimpleMap from "../../../components/map/Map";
import styles from "./Overview.module.scss";

const Overview = (props) => {
  useEffect(() => {
    const { match: { params } } = props;

    console.log('Fetch cost of living overview data with university id: ' + params.id);
  }, [])

  return (
    <div className={styles.overviewContainer}>
      <div className={styles.mapContainer}>
        <SimpleMap/>
      </div>
      <div>
        Overview descriptions
      </div>
    </div>
  )
}

export default Overview;
