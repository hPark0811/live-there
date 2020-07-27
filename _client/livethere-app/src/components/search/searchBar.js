import React, {useEffect, useState} from "react";
import './search.scss';
import {IconButton} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import * as levenshtein from 'js-levenshtein'

// TODO: Componentize search component
const Search = (props) => {
  const [keyword, setKeyword] = useState('');
  const [flatDict, setFlatDict] = useState([]);
  const [matchingTuples, setMatchingTuples] = useState([]);

  useEffect(() => {
    setFlatDict(Object.entries(props.dictToSearch));
  }, [props.dictToSearch])

  useEffect(() => {
    searchKeyword()
  }, [keyword])


  // TODO: Make it generic for future usage
  const searchKeyword = () => {
    if (!keyword || keyword === '') {
      setMatchingTuples([]);
      return;
    }

    for (const [key, val] of flatDict) {
      let universityName = val.universityName.toLowerCase().replace(/\s/g, '');
      let cleanedKeyword = keyword.toLowerCase().replace(/\s/g, '');

      val.score = levenshtein(
        universityName,
        cleanedKeyword
      );

      val.score = Math.abs(val.score - Math.abs(universityName.length - cleanedKeyword.length))
      val.score = val.score / (
        universityName.length > cleanedKeyword.length
          ? cleanedKeyword.length
          : universityName.length
      )
    }

    let count = 0;
    let keys = flatDict
      .sort(([keyA, valA], [keyB, valB]) => valA.score - valB.score)
      .filter(([key, val]) => {
        if (val.score < 0.3 && count < 10) {
          count++;
          return true;
        }
      });

    setMatchingTuples(keys);
  }

  const handleInputChange = (event) => {
    setKeyword(event.target.value);
  }

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      props.handleSearch(keyword);
    }
  }

  const dropdowns = () => {
    return (matchingTuples && matchingTuples.length > 0) ?
      <div className="popup">
        <div className="popup-content">
          {
            matchingTuples.map(([key, val]) => (
              <div className='popup-item'
                   key={key}
                   onClick={() => props.handleSearch(key)}>
                {`${val.universityName}, at ${val.campus} `}
              </div>
            ))
          }
        </div>
      </div>
      : null
  }

  return (
    <>
      <div className='searchBody'>
        <div className="search-content">
          <input
            id="searchBar"
            type="text"
            placeholder="Search your university/college"
            onChange={handleInputChange}
            onKeyUp={handleKeyPress}
          />
          <IconButton id='searchButton'
                      onClick={() => props.handleSearch(keyword)}
                      size='small'>
            <SearchIcon/>
          </IconButton>
        </div>
        {/* TODO: Handle keyboard input to choose*/}
        {dropdowns()}
      </div>
    </>
  );
}

export default Search;
