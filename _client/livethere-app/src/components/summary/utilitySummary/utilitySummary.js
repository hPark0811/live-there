import React, {useEffect, useState} from 'react';
import axios from '../../../axios-wrapper'
import EmojiObjectsIcon from '@material-ui/icons/EmojiObjects';
import {FormControl, FormControlLabel, Checkbox} from '@material-ui/core';
import SummaryLayout from "../../layout/summary/SummaryLayout";
import useIsMountedRef from "../../../util/useIsMountedRef";
import * as actionTypes from "../../../store/actions";
import {connect} from "react-redux";

const UtilitySummary = (props) => {
  const [includeEC, setIncludeEC] = useState(true);
  const [includeNG, setIncludeNG] = useState(true);
  const [summary, setSummary] = useState();
  const isMountedRef = useIsMountedRef();

  useEffect(() => {
    fetchUtilitySummary();
  }, [props]);

  useEffect(() => {
    handleSummaryUpdate(summary);
  }, [includeEC, includeNG]);

  const fetchUtilitySummary = () => {
    console.log('fetch utility summary data');

    let params = {universityId: props.universityDetail.id};

    axios.get(
      `/utility`,
      {
        params: params
      })
      .then(response => {
        console.log('fetched utility summary data');
        if (isMountedRef.current) {
          handleSummaryUpdate(response.data);
        }
      })
      .catch(error => {
        console.error(error);
      })
  }

  const handleSummaryUpdate = (summary) => {
    let totalFee = 0;
    if (includeEC === true) {
      totalFee += summary?.averageEC || 0;
    }
    if (includeNG === true) {
      totalFee += summary?.averageNG || 0;
    }
    setSummary({
      ...summary, totalFee
    });
    props.loadCostOfLivingSummary({
      label: "Utilities",
      estimate: totalFee.toFixed(0)
    })
  }


  const form = summary ? <>
    <FormControl>
      <div>Includes:</div>
      <FormControlLabel
        control={<Checkbox color="primary"
                           checked={includeEC}/>}
        onChange={() => setIncludeEC(prev => !prev)}
        label="Average Electricity"
      />
      <FormControlLabel
        control={<Checkbox color="primary"
                           checked={includeNG}/>}
        onChange={() => setIncludeNG(prev => !prev)}
        label="Average Natural Gas"
      />
    </FormControl>
  </> : null;

  const summaryText = (
    props.universityDetail && summary
      ? <div>
        Estimated utility fee is in the city
        of <b>{props.universityDetail.city}, {props.universityDetail.province}</b> is <b>${summary.totalFee.toFixed(0)}</b>
      </div>
      : <div>No utilities found</div>
  )

  return (
    <SummaryLayout icon={<EmojiObjectsIcon/>}
                   iconText={'UTILITIES'}
                   formElement={form}
                   onSubmit={fetchUtilitySummary}
                   summaryElement={summaryText}/>
  )
}

const mapDispatchToProps = dispatch => {
  return {
    loadCostOfLivingSummary: (payload) => dispatch(actionTypes.loadCostOfLivingSummary(payload))
  }
}

export default connect(null, mapDispatchToProps)(UtilitySummary);

