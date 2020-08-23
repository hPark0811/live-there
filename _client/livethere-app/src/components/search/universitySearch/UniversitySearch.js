import React from "react";
import Search from "../searchBar";
import {connect} from "react-redux";
import {useHistory} from "react-router-dom";

const UniversitySearch = (props) => {
  const history = useHistory();

  const handleSearch = (universityData) => {
    history.push(`/cost-of-living/overview/${universityData.searchKey}`)
  }

  const generateSearchObject = () => {
    return Object.entries(props.universityDict).map(([universityId, universityData]) => ({
      searchKey: universityId,
      searchVal: universityData.universityName
    }))
  }

  const generateDropdownText = (universityData) => {
    const university = props.universityDict[universityData.searchKey];
    return `${university.universityName}, at ${university.campus}`
  }

  return (
    <Search objsToSearch={generateSearchObject()}
            placeHolder="Search your university/college"
            errorMessage="No University was found!"
            handleSearch={handleSearch}
            generateDropdownText={generateDropdownText}/>
  )
}

const mapStateToProps = state => {
  return {
    universityDict: state.universityDict
  }
}

export default connect(mapStateToProps)(UniversitySearch);
