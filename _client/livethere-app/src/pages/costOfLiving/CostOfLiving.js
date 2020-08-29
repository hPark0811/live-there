import React from "react";
import {Redirect, Route, Switch} from "react-router";
import Overview from "./overview/Overview";
import {connect} from "react-redux";

const CostOfLiving = ({selectedUniId, match}) => (
  <Switch>
    <Route path={match.url + "/overview/:id"}
           exact
           component={Overview}>
    </Route>
    <Route path={match.url}>
      <Redirect to={match.url + "/overview/" + selectedUniId}/>
    </Route>
  </Switch>
)

const mapStateToProps = state => {
  return {
    selectedUniId: state.selectedUniId
  }
}

export default connect(mapStateToProps)(CostOfLiving);
