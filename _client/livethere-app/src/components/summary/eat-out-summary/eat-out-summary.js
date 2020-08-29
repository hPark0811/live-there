import React, {useEffect, useState} from 'react';
import SummaryLayout from "../../layout/summary/SummaryLayout";
import RestaurantIcon from '@material-ui/icons/Restaurant';
import Grid from "@material-ui/core/Grid";
import {Checkbox, FormControl, FormControlLabel} from "@material-ui/core";
import FormGroup from "@material-ui/core/FormGroup";
import styles from "../rentalSummary/RentalSummary.module.scss";
import NativeSelect from "@material-ui/core/NativeSelect";

const DEFAULT_SELECTED_PRICE = {
  1: false,
  2: false,
  3: false,
  4: false,
  'ALL': true
}

const EatOutSummary = (props) => {
  const [summary, setSummary] = useState()
  const [maxDistance, setMaxDistance] = useState(15);
  const [minReviews, setMinReviews] = useState(0);

  const [selectedPrices, setSelectedPrices] = useState(DEFAULT_SELECTED_PRICE);

  useEffect(() => {
    fetchEatOutSummary();
  }, [props])

  const fetchEatOutSummary = () => {
    console.log('fetch eat out summary data');
    // TODO(Sami): Make fetch call to eat out summary API here
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
    !!summary ? (
      <div>
        <div>Average eat out price is <b>${summary.average?.toFixed(1)}/meal</b></div>
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
            {['$', '$$', '$$$', '$$$$+'].map((price, ndx) => (
              <FormControlLabel
                control={<Checkbox color="primary"
                                   name={(ndx + 1).toString()}
                                   checked={selectedPrices[ndx + 1]}/>}
                key={ndx}
                onChange={handlePriceChange}
                label={price}
              />
            ))}
            <FormControlLabel
              control={<Checkbox color="primary"
                                 checked={selectedPrices.ALL}
                                 name={'ALL'}/>}
              onChange={handlePriceChange}
              label="ALL"
            />
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

export default EatOutSummary;
