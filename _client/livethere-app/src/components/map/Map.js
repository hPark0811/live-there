import React from 'react';
import GoogleMap from 'google-map-react';

const SimpleMap = (props) => {
  // Important! Always set the container height explicitly
  return (
    <GoogleMap
      bootstrapURLKeys={{key: process.env.REACT_APP_GOOGLE_MAP_API}}
      center={props.center}
      zoom={12}
      onGoogleApiLoaded={({map, maps}) =>
        new maps.Circle({
          strokeWeight: 0,
          fillColor: '#FF0000',
          fillOpacity: 0.2,
          map,
          center: props.center,
          radius: 5000,
        })
      }
    />
  )
};

export default SimpleMap;
