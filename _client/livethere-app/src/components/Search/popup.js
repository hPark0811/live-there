/* components/search/popup.jsx */
import React from "react";
import './search.css';

const Popup = (props) => {
  return (
    <>
      {
        (props.items && props.items.length > 0)
          ? <div className="popup">
              <div className="popup-content">
                {
                  props.items.map((item, index) => {
                    return <div className='popup-item'
                                key={index}
                                onClick={(item) => props.onSearch(item)}>{item}</div>
                  })
                }
              </div>
            </div>
          : null
      }
    </>
  )
}

export default Popup;
