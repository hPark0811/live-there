import React, {useEffect, useState} from "react";
import SimpleMap from "../../../components/map/Map";
import styles from "./Overview.module.scss";
import Utility, {fetchUtilityFee} from "./../../../components/utility/utility"

const Overview = (props) => {
  const [overViewData, setOverViewData] = useState({
    utility: null,
    rental: null
  });

  useEffect(() => {
    const { match: { params } } = props;

    fetchUtilityFee(243).then(response => {  
      setOverViewData({utility: response.data});
    });

    console.log('Fetch cost of living overview data with university id: ' + params.id);
  }, [])

  return (
    <div className={styles.overviewContainer}>
      <div className={styles.mapContainer}>
        <SimpleMap/>
      </div>
      <div>
        <Utility utilityData={overViewData.utility} locationData={ { city: 'London', province: 'ON' } }/>
        Overview descriptions
      </div>
    </div>
  )
}

export default Overview;
