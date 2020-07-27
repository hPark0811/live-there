import * as React from "react";
import Typography from "@material-ui/core/Typography";
import styles from "./Home.module.scss";
import Search from "../../components/search/searchBar";
import * as actionTypes from '../../store/actions.js'
import axios from 'axios'
import {connect} from "react-redux";

/*TODO: Remove from container*/
class Home extends React.Component {
  componentDidMount() {
    axios.get('http://localhost:5000/university')
      .then(response => {
        const universityArr = response.data;
        let universityDict = {};
        universityArr.forEach(university => {
          let uniId = university.id;
          delete university.id;
          universityDict[uniId] = university;
        });
        this.props.onUniversitiesLoaded({
          universityDict
        });
      })
      .catch(error => {
        console.log(error);
      })
  }

  handleSearch = (universityId) => {
    this.props.history.push(`/cost-of-living/overview/${universityId}`)
  }

  render() {
    return (
      <>
        <div className={styles.mainContainer}>
          <div className={styles.descriptionWrapper}>
            <Typography variant="h1"
                        component="h1">
              Explore Your University Area!
            </Typography>
            <Typography variant="subtitle1"
                        component="p">
              LiveThere provides regional research tools based on postgraduate institutions. Get an esimate of living
              cost, utility costs, and more.
            </Typography>
          </div>
          <Search dictToSearch={this.props.universityDict}
                  handleSearch={this.handleSearch}/>
        </div>
        {/* TODO: Add cards */}
      </>
    )
  }
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

export default connect(mapStateToProps, mapDispatchToProps)(Home);
