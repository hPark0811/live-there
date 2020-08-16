import React, {useEffect, useState} from 'react';
import axios from 'axios'
import HouseRoundedIcon from '@material-ui/icons/HouseRounded';
import styles from "./RentalSummary.module.scss";
import {FormControl, FormControlLabel, FormLabel, FormGroup, Checkbox} from '@material-ui/core';
import RadioGroup from "@material-ui/core/RadioGroup";
import Radio from "@material-ui/core/Radio";
import NativeSelect from "@material-ui/core/NativeSelect";
import SummaryLayout from "../../layout/summary/SummaryLayout";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";

const RentalSummary = (props) => {
  const [maxDistance, setMaxDistance] = useState(15);
  const [propertyType, setPropertyType] = useState('');
  const [bathCount, setBathCount] = useState(null);
  const [bedCount, setBedCount] = useState(null);
  const [summary, setSummary] = useState()

  useEffect(() => {
    fetchRentalSummary()
  }, [props]);

  const fetchRentalSummary = () => {
    console.log('fetch rental summary data');

    let params = {universityId: props.universityId};

    if (maxDistance) {
      params.maxDistance = maxDistance;
    }
    if (propertyType) {
      params.propertyType = propertyType;
    }
    if (bathCount) {
      params.bathCount = bathCount;
    }
    if (bedCount) {
      params.bedCount = bedCount;
    }

    axios.get(
      `http://localhost:5000/rental/average`,
      {
        params: params
      })
      .then(response => {
        console.log('fetched rental summary data');
        setSummary(response.data);
      })
      .catch(error => {
        console.error(error);
      })
  }

  const form = (
    <>
      <Grid container>
        <Grid item
              sm={4}
              xs={6}>
          <div>Includes:</div>
          <FormControl component="fieldset">
            <RadioGroup aria-label="propertyType"
                        name="propertyType"
                        value={propertyType}
                        onChange={event => setPropertyType(event.target.value)}>
              {['condo', 'house', 'town house', 'bachelor'].map((type) => (
                <FormControlLabel value={type}
                                  control={<Radio color="primary"/>}
                                  label={type}/>
              ))}
              <FormControlLabel value={""}
                                control={<Radio color="primary"/>}
                                label={'N/A'}/>
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid container
              item
              sm={8}
              xs={6}>
          <Grid item
                xs={12}
                sm={6}>
            <div>Distance:</div>
            <FormControl className={styles.Dropdown}>
              <NativeSelect value={maxDistance}
                            onChange={event => setMaxDistance(parseInt(event.target.value))}>
                {
                  [15, 10, 7, 5, 3, 1].map((maxDistance) => (
                    <option value={maxDistance}>{'< ' + maxDistance + 'km'}</option>
                  ))
                }
              </NativeSelect>
            </FormControl>
          </Grid>
          <Grid item
                xs={12}
                sm={6}>
            <div>Bathrooms:</div>
            <FormControl className={styles.Dropdown}>
              <NativeSelect value={bathCount}
                            onChange={event => setBathCount(parseInt(event.currentTarget.value))}>
                <option value={null}>All</option>
                {
                  [5, 4, 3, 2, 1].map((bathCount) => (
                    <option value={bathCount}>{bathCount}</option>
                  ))
                }
              </NativeSelect>
            </FormControl>
          </Grid>
          <Grid item
                xs={12}
                sm={6}>
            <div>Bedrooms:</div>
            <FormControl className={styles.Dropdown}>
              <NativeSelect value={bedCount}
                            onChange={event => setBedCount(parseInt(event.currentTarget.value))}>
                <option value={null}>All</option>
                {
                  [5, 4, 3, 2, 1].map((bedCount) => (
                    <option value={bedCount}>{bedCount}</option>
                  ))
                }
              </NativeSelect>
            </FormControl>
          </Grid>
        </Grid>
      </Grid>
    </>
  )

  const summaryText = (
    summary && summary.rentalsCount > 0 ? (
      <div>
        <div>Average rental price is <b>${summary.average?.toFixed(0)}/mo per
          room</b></div>
        <div>Calculated with <b>{summary.rentalsCount}</b> listings found online</div>
      </div>
    ) : <div>No listings found!</div>
  )

  return (
    <SummaryLayout icon={<HouseRoundedIcon/>}
                   iconText={'RENTAL'}
                   formElement={form}
                   onSubmit={fetchRentalSummary}
                   summaryElement={summaryText}/>
  )
}

export default RentalSummary;
