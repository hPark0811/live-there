import React, {useEffect, useState} from 'react';
import SummaryLayout from "../../layout/summary/SummaryLayout";
import RestaurantIcon from '@material-ui/icons/Restaurant';
import Grid from "@material-ui/core/Grid";
import {Checkbox, FormControl, FormControlLabel} from "@material-ui/core";
import FormGroup from "@material-ui/core/FormGroup";
import styles from "../rentalSummary/RentalSummary.module.scss";
import NativeSelect from "@material-ui/core/NativeSelect";
import axios from "../../../axios-wrapper";
import useIsMountedRef from "../../../util/useIsMountedRef";
import * as actionTypes from "../../../store/actions";
import {connect} from "react-redux";

const DEFAULT_SELECTED_PRICE = {
  '$': false,
  '$$': false,
  '$$$': false,
  '$$$$': false,
  'ALL': true
}

const EatOutSummary = (props) => {
  const [summary, setSummary] = useState()
  const [maxDistance, setMaxDistance] = useState(15);
  const [minReviews, setMinReviews] = useState(0);
  const [selectedPrices, setSelectedPrices] = useState(DEFAULT_SELECTED_PRICE);

  const isMountedRef = useIsMountedRef();

  useEffect(() => {
    fetchEatOutSummary();
  }, [props])

  const fetchEatOutSummary = () => {
    console.log('fetch eat out summary data');
    let params = {universityId: props.universityId};

    if (maxDistance) {
      params.maxDistance = maxDistance;
    }
    if (minReviews !== '') {
      params.minReviews = minReviews;
    }
    if (selectedPrices) {
      let prices = [];
      Object.entries(selectedPrices).filter(([price, isSelected]) => {
        if (isSelected) {
          prices.push(price);
        }
      })
      params.selectedPrices = prices.toString();
    }

    axios.get(
      `/restaurant/average`,
      {
        params: params
      })
      .then(response => {
        console.log('fetched restaurant summary data');
        if (isMountedRef.current) {
          response.data.average *= 30;
          setSummary(response.data);
          props.loadCostOfLivingSummary({
            label: "Restaurant",
            estimate: response.data.average.toFixed(0)
          })
        }
      })
      .catch(error => {
        console.error(error);
      });
  }

  const handlePriceChange = (event) => {
    let selected = {...selectedPrices};
    if (event.target.name !== 'ALL' && !!event.target.checked) {
      selected.ALL = false;
    } else if (event.target.name === 'ALL' && !!event.target.checked) {
      selected = DEFAULT_SELECTED_PRICE;
    }
    selected[event.target.name] = event.target.checked;
    setSelectedPrices(selected);
  };

  const summaryText = (
    !!summary && summary.average? (
      <div>
        <div>Average eat out price is <b>${summary.average.toFixed(1)}/month</b></div>
      <div>Calculated from<b>{summary.restaurantCount}</b> restaurants in area</div>
      </div>
    ) : <div>No restaurant data found!</div>
  )

  const form = (
    <>
      <Grid container>
        <Grid item
              sm={4}
              xs={6}>
          <div>Prices:</div>
          <FormGroup>
            {Object.keys(DEFAULT_SELECTED_PRICE).map((price, ndx) => (
              <FormControlLabel
                control={<Checkbox color="primary"
                                   name={price}
                                   checked={selectedPrices[price]}/>}
                key={ndx}
                onChange={handlePriceChange}
                label={price}
              />
            ))}
          </FormGroup>
        </Grid>
        <Grid container
              item
              sm={8}
              xs={6}>
          <Grid item
                xs={12}
                sm={12}>
            <div>Distance:</div>
            <FormControl className={styles.Dropdown}>
              <NativeSelect value={maxDistance}
                            onChange={event => setMaxDistance(parseInt(event.target.value))}>
                {
                  [15, 10, 7, 5, 3, 1].map((maxDistance, ndx) => (
                    <option key={ndx}
                            value={maxDistance}>{'< ' + maxDistance + 'km'}</option>
                  ))
                }
              </NativeSelect>
            </FormControl>
          </Grid>
          <Grid item
                xs={12}
                sm={12}>
            <div>Reviews:</div>
            <FormControl className={styles.Dropdown}>
              <NativeSelect value={minReviews}
                            onChange={event => setMinReviews(parseInt(event.target.value))}>
                {
                  [1000, 500, 300, 200, 100, 0].map((minReviews, ndx) => (
                    <option key={ndx}
                            value={minReviews}>{minReviews + ' +'}</option>
                  ))
                }
              </NativeSelect>
            </FormControl>
          </Grid>
        </Grid>
      </Grid>
    </>
  )

  return (
    <SummaryLayout icon={<RestaurantIcon/>}
                   iconText={'EATING OUT'}
                   formElement={form}
                   onSubmit={fetchEatOutSummary}
                   summaryElement={summaryText}/>
  )
}

const mapDispatchToProps = dispatch => {
  return {
    loadCostOfLivingSummary: (payload) => dispatch(actionTypes.loadCostOfLivingSummary(payload))
  }
}

export default connect(null, mapDispatchToProps)(EatOutSummary);
