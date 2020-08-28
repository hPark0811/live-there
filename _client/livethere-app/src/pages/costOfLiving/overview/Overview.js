import React, {useEffect, useState} from "react";
import SimpleMap from "../../../components/map/Map";
import styles from "./Overview.module.scss";
import axios from "../../../axios-wrapper";
import RentalSummary from "../../../components/summary/rentalSummary/RentalSummary";
import UtilitySummary from "../../../components/summary/utilitySummary/utilitySummary"
import UniversitySearch from "../../../components/search/universitySearch/UniversitySearch";
import EatOutSummary from "../../../components/summary/eat-out-summary/eat-out-summary";

const Overview = (props) => {
  const [universityDetail, setUniversityDetail] = useState();

  useEffect(() => {
    const {match: {params}} = props;

    console.log('Fetch cost of living overview data with university id: ' + params.id);
    axios.get(`/university/${params.id}`)
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
        <div className={styles.searchContainer}>
          <UniversitySearch/>
        </div>
        <div className={styles.summaryList}>
          <RentalSummary universityId={universityDetail.id}/>
          <UtilitySummary universityDetail={universityDetail}/>
          <EatOutSummary universityId={universityDetail.id}/>
        </div>
      </div>
    </div>
    : null;
}

export default Overview;
