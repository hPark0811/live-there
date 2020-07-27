import React from 'react';
import {BrowserRouter} from "react-router-dom";
import {Route, Switch} from "react-router"
import {ThemeProvider} from '@material-ui/core/styles';
import mainTheme from "./assets/styles/_theme";
import Layout from "./components/layout/Layout";
import Home from "./pages/home/Home";
import CostOfLiving from "./pages/costOfLiving/CostOfLiving";

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider theme={mainTheme}>
        <Layout>
          <Switch>
            <Route path="/" exact component={Home}/>
            <Route path="/cost-of-living" component={CostOfLiving}/>
          </Switch>
        </Layout>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
