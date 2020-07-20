import React from "react";
import Popup from "./popup";
import { dummyFetchPopupItems } from './../../server/dummyServer';
import './searchBar.css';


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
                type="text"
                placeholder="Search your university/college"
                onChange={ this.handleInputChange }
                onKeyUp={ this.handleKeyPress }
            />
            <button onClick={()=>this.searchByKey(this.state.keyword)}> Search </button>
            <Popup items={this.state.popupItem} searchFunc={this.searchByKey}/>
        </div>
      </div>
    );
  }
}