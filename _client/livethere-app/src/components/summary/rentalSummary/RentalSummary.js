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
import useIsMountedRef from "../../../util/useIsMountedRef";
import * as actionTypes from "../../../store/actions";
import {connect} from "react-redux";

const RentalSummary = (props) => {
  const [maxDistance, setMaxDistance] = useState(15);
  const [propertyType, setPropertyType] = useState('');
  const [bathCount, setBathCount] = useState('');
  const [bedCount, setBedCount] = useState('');
  const [summary, setSummary] = useState();
  const isMountedRef = useIsMountedRef();

  useEffect(() => {
    fetchRentalSummary();
  }, [props]);

  const fetchRentalSummary = () => {
    let params = {
      universityId: props.universityId,
      postalCode: props.postalCode.slice(0, 3) + " " + props.postalCode.slice(3)
    }
    // TODO: move this to backend.
    if (maxDistance) {
      params.maxDistance = maxDistance;
    }
    if (propertyType !== '') {
      params.propertyType = propertyType;
    }
    if (bathCount !== '' && !isNaN(bathCount)) {
      params.bathCount = bathCount;
    }
    if (bedCount !== '' && !isNaN(bedCount)) {
      params.bedCount = bedCount;
    }

    axios.get('/rental/summary', {params: params})
      .then(response => {
        console.log('RECEIVED', response.data);
        if (isMountedRef.current) {
          setSummary(response.data);
          let estimate = response.data.metric !== 'na' ? response.data.estimate : 0;
          props.loadCostOfLivingSummary({
            label: 'Rental',
            estimate: estimate.toFixed(0)
          });
        }
      })
      .catch(error => {
        console.error(error);
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
              <FormControlLabel value={''}
                                control={<Radio color="primary"/>}
                                label={'ALL'}/>
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
                  [15, 10, 5, 1].map((maxDistance, ndx) => (
                    <option key={ndx}
                            value={maxDistance}>{'< ' + maxDistance + 'km'}</option>
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
                  [3, 2, 1].map((bathCount, ndx) => (
                    <option key={ndx}
                            value={bathCount}>{bathCount}</option>
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
                    <option key={ndx}
                            value={bedCount}>{bedCount}</option>
                  ))
                }
              </NativeSelect>
            </FormControl>
          </Grid>
        </Grid>
      </Grid>
    </>
  )

  let summaryText;

  switch (summary?.metric) {
    case 'average':
      summaryText = (
        <div>
          <div>
            Average rental price is <b>${summary.estimate?.toFixed(0)}/month per room</b>
          </div>
          <div>
            Calculated with <b>{summary.rentalsCount}</b> listings found online.
          </div>
        </div>
      );
      break;
    case 'prediction':
      summaryText = (
        <div>
          Predicted rental price is <b>${summary.estimate?.toFixed(0)}/month per room</b>
        </div>
      );
      break;
    default: // case 'na': 
      summaryText = <div>No listings found!</div>
  }

  return (
    <SummaryLayout icon={<HouseRoundedIcon/>}
                   iconText={'RENTAL'}
                   formElement={form}
                   onSubmit={fetchRentalSummary}
                   summaryElement={summaryText}/>
  )
}

const mapDispatchToProps = dispatch => {
  return {
    loadCostOfLivingSummary: (payload) => dispatch(actionTypes.loadCostOfLivingSummary(payload))
  }
}

export default connect(null, mapDispatchToProps)(RentalSummary);
