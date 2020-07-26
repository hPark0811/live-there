import React, {useEffect, useState} from "react";
import Popup from "./popup";
import {dummyFetchPopupItems} from '../../util/dummyServer';
import './search.scss';
import {IconButton} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';

const Search = (props) => {
  const [keyword, setKeyword] = useState('');
  const [popupList, setPopupList] = useState([]);
  const [showPopup, setShowPopup] = useState(true);

  useEffect(() => {
    dummyFetchPopupItems(keyword)
      .then(popupItems => {
        setPopupList(popupItems);
      })
      .catch(err => {
        console.error('Error connecting to search backend', err);
      });
  }, [keyword])

  const handleInputChange = (event) => {
    setKeyword(event.target.value);
  }

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      search();
    }
  }

  const search = (recommendedKeyword = keyword) => {
    console.log(`Search with keyword ${recommendedKeyword}`)
  }

  return (
    <div className='searchBody'>
      <div className="search-content">
        <input
          id="searchBar"
          type="text"
          placeholder="Search your university/college"
          onChange={handleInputChange}
          onKeyUp={handleKeyPress}
          onFocus={() => setShowPopup(true)}
          onBlur={() => setShowPopup(false)}
        />
        <IconButton id='searchButton'
                    onClick={search}
                    size='small'>
          <SearchIcon/>
        </IconButton>
      </div>
      {/* TODO: Handle keyboard input to choose*/}
      <Popup show={showPopup}
             items={popupList}
             onSearch={search}/>
    </div>
  );
}

export default Search;
