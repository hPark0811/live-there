import React, {useEffect} from 'react';
import {BrowserRouter} from "react-router-dom";
import {Route, Switch} from "react-router"
import {ThemeProvider} from '@material-ui/core/styles';
import mainTheme from "./assets/styles/_theme";
import Home from "./pages/home/Home";
import CostOfLiving from "./pages/costOfLiving/CostOfLiving";
import PageLayout from "./components/layout/page/PageLayout";
import * as actionTypes from "./store/actions";
import {connect} from "react-redux";
import axios from "./axios-wrapper";

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
          </Switch>
        </PageLayout>
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
