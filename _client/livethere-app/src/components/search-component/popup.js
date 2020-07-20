/* components/search/popup.jsx */
import React from "react";

export default class Popup extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { items, searchFunc } = this.props;
    // When empty show nothing
    if (items.length===0) return null; 
    return (
      <div className="popup">
          <div className="popup-content">
            {
              items.map((item, index) => {
                return <div className='item' key={index} onClick={()=> searchFunc(item)}> {item} </div>
              })
            }
          </div>
      </div>
    );
  }
}