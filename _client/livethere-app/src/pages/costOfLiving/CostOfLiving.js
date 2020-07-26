import React from "react";
import {Route} from "react-router";

const CostOfLiving = ({match}) => (
  <>
    <Route path={match.url + "/overview/uwo"}
           exact>
      {/*<Overview/>*/}
    </Route>
  </>
)

export default CostOfLiving;
