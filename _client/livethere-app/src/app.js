import React from 'react';
import {BrowserRouter, Route, Switch} from "react-router-dom";
import {ThemeProvider} from '@material-ui/core/styles';
import mainTheme from "./assets/styles/_theme";
import Layout from "./components/Layout/Layout";
import Home from "./containers/home/Home";

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider theme={mainTheme}>
        <Layout>
          <Switch>
            <Route path="/" exact>
              <Home/>
            </Route>
          </Switch>
        </Layout>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
