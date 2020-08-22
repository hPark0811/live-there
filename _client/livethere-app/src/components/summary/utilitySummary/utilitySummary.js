import React, {useEffect, useState} from 'react';
import axios from '../../../axios-wrapper'
import EmojiObjectsIcon from '@material-ui/icons/EmojiObjects';
import {FormControl, FormControlLabel, Checkbox} from '@material-ui/core';
import SummaryLayout from "../../layout/summary/SummaryLayout";

const UtilitySummary = (props) => {
  const [includeEC, setIncludeEC] = useState(true);
  const [includeNG, setIncludeNG] = useState(true);
  const [summary, setSummary] = useState();

  useEffect(() => {
    fetchUtilitySummary()
  }, [props]);

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
        setSummary(response.data);
      })
      .catch(error => {
        console.error(error);
      })
  }

  let totalFee = 0;
  if (includeEC === true) {
    totalFee += summary?.averageEC || 0;
  }
  if (includeNG === true) {
    totalFee += summary?.averageNG || 0;
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
    props.universityDetail
      ? <div>
        Estimated utility fee is in the city of <b>{props.universityDetail.city}, {props.universityDetail.province}</b> is <b>${totalFee.toFixed(0)}</b>
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

export default UtilitySummary;

