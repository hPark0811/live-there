import React, {useEffect, useState} from 'react';
import {Pie} from "react-chartjs-2";
import {connect} from "react-redux";
import _ from "lodash"
import Typography from "@material-ui/core/Typography";

const DEFAULT_DATA = {
  labels: [],
  datasets: [{
    data: [],
    backgroundColor: [
      '#36A2EB',
      '#FF6384',
      '#FFCE56'
    ],
    hoverBackgroundColor: [
      '#36A2EB',
      '#FF6384',
      '#FFCE56'
    ]
  }],
};

const DEFAULT_LEGEND = {
  "position": "bottom",
  "fullWidth": true,
  "labels": {
    "fontColor": "black",
    "fontSize": 16,
  },
}

const SummaryChart = (props) => {
  const [data, setData] = useState(null);
  const [sum, setSum] = useState(0);

  useEffect(() => {
    const tempData = _.cloneDeep(DEFAULT_DATA);
    let sum = 0;

    tempData.labels = [];
    tempData.datasets[0].data = [];
    for (const [label, estimate] of Object.entries(props.costOfLivingMap)) {
      tempData.labels.push(label);
      tempData.datasets[0].data.push(estimate);
      sum += +estimate;
    }
    console.log(tempData);
    setData(tempData);
    setSum(sum);
  }, [props.costOfLivingMap])

  // TODO: Make message customizable for reusability of pie graph
  return (
    <>
      <Typography variant='h4'>Total Estimated Cost: ${sum} </Typography>
      <br/>
      {data && <Pie data={data}
                    legend={DEFAULT_LEGEND}/>}
    </>
  )
}

const mapStateToProps = state => {
  return {
    costOfLivingMap: state.costOfLiving
  }
}

export default connect(mapStateToProps)(SummaryChart);
