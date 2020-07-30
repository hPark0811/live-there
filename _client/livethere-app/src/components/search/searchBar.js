import React, {useEffect, useState} from "react";
import './search.scss';
import {IconButton} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import * as levenshtein from 'js-levenshtein'

// TODO: WRITE MORE COMMENTS.
// TODO: Componentize search component
const Search = (props) => {
  /* state and setState*/
  const [keyword, setKeyword] = useState('');
  const [flatDict, setFlatDict] = useState([]);
  const [matchingTuples, setMatchingTuples] = useState([]);
  const [dropDownIndx, setDropDownIndx] = useState(-1);
  const [showDropbox, setShowDropbox] = useState(false);

  /* hooks */
  useEffect(() => {
    setFlatDict(Object.entries(props.dictToSearch));
  }, [props.dictToSearch])

  useEffect(() => {
    searchKeyword()
  }, [keyword])


  // TODO: Make it generic for future usage
  /* utils */
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

  const selectDropdown = (index) => {
    // Wrapper of setDropDownIndx with index condition.
    if (index >= 0 && index < matchingTuples.length)
      setDropDownIndx(index);
  }

  /* event handler */
  const handleSearchByKeyword = (word) => {
    if (keyword !== word) setKeyword(word);    
    if (matchingTuples && matchingTuples.length > 0){
      const [key, val] = matchingTuples[0]
      props.handleSearch(key);
    }
    else{
      alert('No University was found!');
    }
  }

  const handleSearchByKey = (key) =>{
    props.handleSearch(key);
  }

  const handleInputChange = (event) => {
    setShowDropbox(true);
    setKeyword(event.target.value);
  }

  const handleOnBlur = () => {
    // OnBlur reset matching tuple and dropDownIndx.
    setShowDropbox(false);
    setDropDownIndx(-1);
  }

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      if (dropDownIndx !== -1 && showDropbox){
        // If dropDownIndx is selected and dropbox is shown => search by dropbox index.
        const [key, val] = matchingTuples[dropDownIndx];
        handleSearchByKey(key);
      }
      else{
        // If dropdown index is not selected or drop box is not shown, search by keyword
        handleSearchByKeyword(keyword);
      }
    }
    if (event.key ==='ArrowUp'){
      selectDropdown(dropDownIndx-1);
    }
    if (event.key === 'ArrowDown'){
      selectDropdown(dropDownIndx+1);
    }
  }

  // Dropdown inner component. 
  const Dropdown = (props) => {
    return (showDropbox && matchingTuples && matchingTuples.length > 0) ?
      <div className="popup" onClick={()=>{console.log(1)}}>
        <div className="popup-content">
          {
            matchingTuples.map(([key, val], i) => {
              return (
                <div className={dropDownIndx === i ? 'popup-item:hover' : 'popup-item'}
                     key={key}
                     onClick={() => handleSearchByKey(key)}>
                  {`${val.universityName}, at ${val.campus} `}
                </div>
              )
            })
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
            onBlur={handleOnBlur}
            onClick={()=>{ if (keyword !== '') setShowDropbox(true)}}
          />
          <IconButton id='searchButton'
                      onClick={() => handleSearchByKeyword(keyword)}
                      size='small'>
            <SearchIcon/>
          </IconButton>
        </div>
        <Dropdown/>
      </div>
    </>
  );
}

export default Search;
