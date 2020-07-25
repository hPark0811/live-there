import React, {useState} from "react";
import Popup from "./popup";
import {dummyFetchPopupItems} from '../../util/dummyServer';
import './search.css';
import {IconButton} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';


const Search = (props) => {
  const [keyword, setKeyword] = useState('');
  const [popupList, setPopupList] = useState([]);

  const handleInputChange = (event) => {
    setKeyword(event.target.value);
    dummyFetchPopupItems(keyword)
      .then(popupItems => {
        setPopupList(popupItems);
      })
      .catch(err => {
        console.error('Error connecting to search backend', err);
      })
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
        />
        <IconButton id='searchButton'
                    onClick={search}
                    size='small'>
          <SearchIcon/>
        </IconButton>
      </div>
      <Popup items={popupList}
             onSearch={search}/>
    </div>
  );
}

export default Search;
