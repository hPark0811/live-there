import React, {useEffect, useState} from "react";
import SimpleMap from "../../../components/map/Map";
import styles from "./Overview.module.scss";
import axios from "../../../axios-wrapper";
import RentalSummary from "../../../components/summary/rentalSummary/RentalSummary";
import UtilitySummary from "../../../components/summary/utilitySummary/utilitySummary"
import UniversitySearch from "../../../components/search/universitySearch/UniversitySearch";
import EatOutSummary from "../../../components/summary/eat-out-summary/eat-out-summary";
import {connect} from "react-redux";
import * as actionTypes from "../../../store/actions";
import {useHistory} from "react-router";
import useIsMountedRef from "../../../util/useIsMountedRef";
import SummaryGraph from "../../../components/summary/summary-chart/summary-chart";

const Overview = (props) => {
  const history = useHistory();
  const [universityDetail, setUniversityDetail] = useState();
  const isMountedRef = useIsMountedRef();

  useEffect(() => {
    props.showSnackBar({
      message: "Map's radius is 3KM",
      duration: 8000,
      severity: "info"
    })
  }, [])

  useEffect(() => {
    const {match: {params}} = props;

    console.log('Fetch cost of living overview data with university id: ' + params.id);
    axios.get(`/university/${params.id}`)
      .then(response => {
        if (isMountedRef.current) {
          setUniversityDetail(response.data);
          props.selectUniversity({selectedUniId: params.id});
        }
      })
      .catch(error => {
        console.error(error);
        history.push("/error");
      });
  }, [props, isMountedRef, history])

  return universityDetail && isMountedRef.current ?
    <div className={styles.overviewContainer}>
      <div className={styles.mapContainer}>
        <SimpleMap center={{lat: universityDetail.latitude, lng: universityDetail.longitude}}/>
      </div>
      <div className={styles.listContainer}>
        <div className={styles.searchContainer}>
          <UniversitySearch/>
          <div className={styles.chart}>
            <SummaryGraph/>
          </div>
        </div>
        <div className={styles.summaryList}>
          <RentalSummary universityId={universityDetail.id}
                         postalCode={universityDetail.postalCode}/>
          <UtilitySummary universityDetail={universityDetail}/>
          <EatOutSummary universityId={universityDetail.id}/>
        </div>
      </div>
    </div>
    : null;
}

const mapStateToProps = state => {
  return {
    selectedUniId: state.selectedUniId
  }
}

const mapDispatchToProps = dispatch => {
  return {
    selectUniversity: (payload) => dispatch(actionTypes.selectUniversity(payload)),
    showSnackBar: (payload) => dispatch(actionTypes.showSnackBar(payload))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Overview);
