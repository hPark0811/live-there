import React, {useEffect, useState} from 'react';
import HouseRoundedIcon from '@material-ui/icons/HouseRounded';
import styles from "./RentalSummary.module.scss";
import {FormControl, FormControlLabel} from '@material-ui/core';
import RadioGroup from "@material-ui/core/RadioGroup";
import Radio from "@material-ui/core/Radio";
import NativeSelect from "@material-ui/core/NativeSelect";
import SummaryLayout from "../../layout/summary/SummaryLayout";
import Grid from "@material-ui/core/Grid";
import axios from '../../../axios-wrapper';


const RentalSummary = (props) => {
  const [maxDistance, setMaxDistance] = useState(15);
  const [propertyType, setPropertyType] = useState('');
  const [bathCount, setBathCount] = useState('');
  const [bedCount, setBedCount] = useState('');
  const [summary, setSummary] = useState();
  // TODO: append prediction to summary?
  const [prediction, setPrediction] = useState();

  useEffect(() => {
    fetchRentalSummary();
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
    if (bathCount !== '') {
      params.bathCount = bathCount;
    }
    if (bedCount !== '') {
      params.bedCount = bedCount;
    }

    axios.get(
      `/rental/average`,
      {
        params: params
      })
      .then(response => {
        console.log('fetched rental summary data');
        setSummary(response.data);
      })
      .catch(error => {
        console.error(error);
      });
    
    fetchRentalPrediction();
  }

  const fetchRentalPrediction = () => {
    console.log('fetch rental prediction');

    let params = {
      universityId: props.universityId
    };

    params.propertyType = propertyType ? propertyType : 'condo';
    params.bathCount = bathCount !== '' ? bathCount : 0;
    params.bedCount = bedCount !== '' ? bedCount : 0;
    params.postalCode = props.postalCode.slice(0, 3) + " " + props.postalCode.slice(3);

    axios.get(
      '/rental/predict',
      {
        params: params
      }
    )
    .then(response => {
      console.log('fetched rental prediction data');
      setPrediction(response.data);
    })
    .catch(err => {
      console.log(err);
    });
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
              {['condo', 'house', 'town house', 'bachelor'].map((type, ndx) => (
                <FormControlLabel value={type}
                                  key={ndx}
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
                  [15, 10, 7, 5, 3, 1].map((maxDistance, ndx) => (
                    <option key={ndx} value={maxDistance}>{'< ' + maxDistance + 'km'}</option>
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
                            onChange={event => setBathCount(parseInt(event.target.value))}>
                <option value={''}>All</option>
                {
                  [5, 4, 3, 2, 1].map((bathCount, ndx) => (
                    <option key={ndx} value={bathCount}>{bathCount}</option>
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
                            onChange={event => setBedCount(parseInt(event.target.value))}>
                <option value={''}>All</option>
                {
                  [5, 4, 3, 2, 1].map((bedCount, ndx) => (
                    <option key={ndx} value={bedCount}>{bedCount}</option>
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
    <div>
      <div>
        {
          summary && summary.rentalsCount > 0 ? (
          <div>
            <div>
              Average rental price is <b>${summary.average?.toFixed(0)}/mo per room</b>
            </div>
          <div>
            Calculated with <b>{summary.rentalsCount}</b> listings found online
          </div>
        </div>
        ) : <div>No listings found!</div>
        }
      </div>
      <div>
        {
          prediction ? (
            <div>
              Predicted rental price is <b>${prediction.prediction?.toFixed(0)}/mo per room</b>
            </div>
          ): null
        }
      </div>
    </div>
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
