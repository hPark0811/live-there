import React from 'react';
import Snackbar from "@material-ui/core/Snackbar";
import Alert from "@material-ui/lab/Alert";
import * as actionTypes from "../../store/actions";
import {connect} from "react-redux";
import {makeStyles} from "@material-ui/core/styles";

function CustomAlert(props) {
  return <Alert elevation={6}
                variant="filled" {...props} />;
}

const useStyles = makeStyles(() => ({
  message: {
    fontSize: "1rem"
  },
}));

const CustomSnackBar = (props) => {
  const classes = useStyles();
  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    props.closeSnackBar();
  };

  return (
    <Snackbar open={props.show}
              autoHideDuration={props.duration}
              onClose={handleClose}>
      <CustomAlert onClose={handleClose}
                   severity={props.severity}>
        <b className={classes.message}>{props.message}</b>
      </CustomAlert>
    </Snackbar>
  )
}

const mapStateToProps = state => {
  return {
    ...state.snackBar
  }
}

const mapDispatchToProps = dispatch => {
  return {
    closeSnackBar: () => dispatch(actionTypes.closeSnackBar())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(CustomSnackBar);
