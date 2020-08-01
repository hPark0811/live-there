import React from "react";
import {Route} from "react-router";
import Overview from "./overview/Overview";

const CostOfLiving = ({match}) => (
  <>
    <Route path={match.url + "/overview/:id"}
           exact
           component={Overview}>
    </Route>
  </>
)

export default CostOfLiving;
