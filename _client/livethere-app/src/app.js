import React from 'react';
import {BrowserRouter} from "react-router-dom";
import {Route, Switch} from "react-router"
import {ThemeProvider} from '@material-ui/core/styles';
import mainTheme from "./assets/styles/_theme";
import Home from "./pages/home/Home";
import CostOfLiving from "./pages/costOfLiving/CostOfLiving";
import PageLayout from "./components/layout/page/PageLayout";

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider theme={mainTheme}>
        <PageLayout>
          <Switch>
            <Route path="/" exact component={Home}/>
            <Route path="/cost-of-living" component={CostOfLiving}/>
          </Switch>
        </PageLayout>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
