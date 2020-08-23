import React, {useEffect, useState} from "react";
import './searchBar.scss';
import {IconButton} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import * as levenshtein from 'js-levenshtein'

const Search = (props) => {
  /* state and setState*/
  const [keyword, setKeyword] = useState('');
  const [matchingData, setMatchingData] = useState([]);
  const [dropDownNdx, setDropDownNdx] = useState(-1);
  const [showDropbox, setShowDropbox] = useState(false);

  useEffect(() => {
    searchKeyword()
  }, [keyword])

  const searchKeyword = () => {
    if (!keyword || keyword === '') {
      setMatchingData([]);
      return;
    }

    for (const data of props?.objsToSearch) {
      let strToCompare = data.searchVal.toLowerCase().replace(/\s/g, '');
      let cleanedKeyword = keyword.toLowerCase().replace(/\s/g, '');

      data.score = levenshtein(
        strToCompare,
        cleanedKeyword
      );

      data.score = Math.abs(data.score - Math.abs(strToCompare.length - cleanedKeyword.length))
      data.score = data.score / (
        strToCompare.length > cleanedKeyword.length
          ? cleanedKeyword.length
          : strToCompare.length
      )
    }

    let count = 0;
    let topMatches = props?.objsToSearch
      .sort((dataA, dataB) => dataA.score - dataB.score)
      .filter((data) => {
        if (data.score < 0.3 && count < 10) {
          count++;
          return true;
        }
      });

    setMatchingData(topMatches);
  }

  const selectDropdown = (index) => {
    // Wrapper of setDropDownIndx with index condition.
    if (index >= 0 && index < matchingData.length)
      setDropDownNdx(index);
  }

  const handleSearch = (data) => {
    setKeyword('');
    setShowDropbox(false);
    props.handleSearch(data);
  }

  /* event handler */
  const handleSearchByKeyword = (word) => {
    if (keyword !== word) setKeyword(word);
    if (matchingData && matchingData.length > 0) {
      handleSearch(matchingData[0]);
    } else {
      alert(props.errorMessage);
    }
  }

  const handleInputChange = (event) => {
    setShowDropbox(true);
    setKeyword(event.target.value);
  }

  const handleOnBlur = () => {
    // OnBlur reset matching tuple and dropDownIndx.
    setShowDropbox(false);
    setDropDownNdx(-1);
  }

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      if (dropDownNdx !== -1 && showDropbox) {
        // If dropDownIndx is selected and dropbox is shown => search by dropbox index.
        handleSearch(matchingData[dropDownNdx]);
      } else {
        // If dropdown index is not selected or drop box is not shown, search by keyword
        handleSearchByKeyword(keyword);
      }
    }
    if (event.key === 'ArrowUp') {
      selectDropdown(dropDownNdx - 1);
    }
    if (event.key === 'ArrowDown') {
      selectDropdown(dropDownNdx + 1);
    }
  }

  // Dropdown inner component.
  const Dropdown = () => {
    return (showDropbox && matchingData && matchingData.length > 0) ?
      <div className="popup">
        <div className="popup-content">
          {
            matchingData.map((data, i) => {
              return (
                <div className={dropDownNdx === i ? 'popup-item:hover' : 'popup-item'}
                     key={data.searchKey}
                     onMouseDown={() => handleSearch(data)}>
                  {props.generateDropdownText(data)}
                </div>
              )
            })
          }
        </div>
      </div>
      : null
  }

  return (
    <div className='search-container'>
      <div className="search-content">
        <input
          id="searchBar"
          type="text"
          autoComplete="off"
          placeholder={props.placeHolder}
          onChange={handleInputChange}
          onKeyUp={handleKeyPress}
          value={keyword}
          onClick={() => {
            if (keyword !== '') setShowDropbox(true)
          }}
          onBlur={handleOnBlur}
        />
        <IconButton id='searchButton'
                    onClick={() => handleSearchByKeyword(keyword)}
                    size='small'>
          <SearchIcon/>
        </IconButton>
      </div>
      <Dropdown/>
    </div>
  );
}

export default Search;
