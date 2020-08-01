import React from 'react';
import GoogleMap from 'google-map-react';

// TODO: Set center, zoom, circle radius from parent
const defaultProps = {
  center: {
    lat: 43.007283,
    lng: -81.275624
  },
  zoom: 14
};

const SimpleMap = ({props = defaultProps}) => {
  // Important! Always set the container height explicitly
  return (
    <GoogleMap
      bootstrapURLKeys={{key: ''}}
      defaultCenter={props.center}
      defaultZoom={props.zoom}
      onGoogleApiLoaded={({map, maps}) =>
        new maps.Circle({
          strokeWeight: 0,
          fillColor: '#FF0000',
          fillOpacity: 0.2,
          map,
          center: props.center,
          radius: 3000,
        })
      }
    />
  )
};

export default SimpleMap;
