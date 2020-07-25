import React from "react";
import Popup from "./popup";
import { dummyFetchPopupItems } from './../../server/dummyServer';
import './search.css';
import { IconButton } from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';


export default class Search extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        "keyword": '', 
        "popupItem": [],
    };
    this.handleInputChange = this.handleInputChange.bind(this);
  }

  handleInputChange = (event) => {
      let newKey = event.target.value;
      // TODO: when to send search ?
      if(newKey===''){
          this.setState({'keyword':'', popupItem:[]})
      }
      else{
        dummyFetchPopupItems().then((popupItems=>{
            this.setState({ 'keyword': newKey, 'popupItem': popupItems});      
        }));
      }
  }

  handleKeyPress = (event) => {
      if(event.key === 'Enter'){
          this.searchByKey(this.state.keyword)
      }
  }

  searchByKey = (keyword) => {
      console.log(`Search with keyword ${keyword}`)
  }

  render() {
    return (
      <div className='searchBody'>
        <div className="search-content">
            <input
                id="searchBar"
                type="text"
                placeholder="Search your university/college"
                onChange={ this.handleInputChange }
                onKeyUp={ this.handleKeyPress }
            />
            <IconButton id='searchButton' onClick={()=>this.searchByKey(this.state.keyword)} size='small'> <SearchIcon/> </IconButton>
        </div>   
        <Popup items={this.state.popupItem} searchFunc={this.searchByKey}/>

      </div>
    );
  } 
}