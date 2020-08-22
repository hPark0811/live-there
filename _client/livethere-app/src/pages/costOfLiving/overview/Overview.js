import React, {useEffect, useState} from "react";
import SimpleMap from "../../../components/map/Map";
import styles from "./Overview.module.scss";
import axios from "axios";
import RentalSummary from "../../../components/summary/rentalSummary/RentalSummary";
import UtilitySummary from "../../../components/summary/utilitySummary/utilitySummary"

const Overview = (props) => {
  const [universityDetail, setUniversityDetail] = useState();

  useEffect(() => {
    const { match: { params } } = props;

    console.log('Fetch cost of living overview data with university id: ' + params.id);
    axios.get(`http://localhost:5000/university/${params.id}`)
      .then(response => {
        setUniversityDetail(response.data);
      })
      .catch(error => {
        console.error(error);
      })

  }, [props])

  return universityDetail ?
    <div className={styles.overviewContainer}>
      <div className={styles.mapContainer}>
        <SimpleMap center={{lat: universityDetail.latitude, lng: universityDetail.longitude}}/>
      </div>
      <div className={styles.listContainer}>
        <RentalSummary universityId={universityDetail.id}/>
        <UtilitySummary universityDetail={universityDetail}/>
      </div>
    </div>
    : null;
}

export default Overview;
