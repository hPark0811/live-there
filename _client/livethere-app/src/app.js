import React, {useEffect} from 'react';
import {BrowserRouter} from "react-router-dom";
import {Redirect, Route, Switch} from "react-router"
import {ThemeProvider} from '@material-ui/core/styles';
import mainTheme from "./assets/styles/_theme";
import Home from "./pages/home/Home";
import CostOfLiving from "./pages/costOfLiving/CostOfLiving";
import PageLayout from "./components/layout/page/PageLayout";
import * as actionTypes from "./store/actions";
import {connect} from "react-redux";
import axios from "./axios-wrapper";
import NotFound from "./pages/error/not-found/not-found";
import AboutUs from "./pages/about-us/about-us";
import CustomSnackBar from "./components/custom-snack-bar/custom-snack-bar";

function App(props) {
  useEffect(() => {
    loadUniversities();
  }, []);

  const loadUniversities = () => {
    axios.get('/university')
      .then(response => {
        const universityArr = response.data;
        let universityDict = {};
        universityArr.forEach(university => {
          let uniId = university.id;
          delete university.id;
          universityDict[uniId] = university;
        });
        props.onUniversitiesLoaded({
          universityDict
        });
      })
      .catch(error => {
        console.log(error);
      })
  }

  return (
    <BrowserRouter>
      <ThemeProvider theme={mainTheme}>
        <PageLayout>
          <Switch>
            <Route path="/"
                   exact
                   component={Home}/>
            <Route path="/cost-of-living"
                   component={CostOfLiving}/>
            <Route path="/error"
                   exact
                   component={NotFound}/>
            <Route path="/about-us"
                   exact
                   component={AboutUs}/>
            <Route path="/">
              <Redirect to="/error"/>
            </Route>
          </Switch>
        </PageLayout>
        <CustomSnackBar/>
      </ThemeProvider>
    </BrowserRouter>
  );
}

const mapStateToProps = state => {
  return {
    universityDict: state.universityDict
  }
}

const mapDispatchToProps = dispatch => {
  return {
    onUniversitiesLoaded: (payload) => dispatch(actionTypes.loadUniversities(payload))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
