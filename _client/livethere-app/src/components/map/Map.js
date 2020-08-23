import React, {useEffect, useState} from 'react';
import GoogleMap from 'google-map-react';

const SimpleMap = (props) => {
  const [map, setMap] = useState();
  const [maps, setMaps] = useState();
  const [circle, setCircle] = useState();

  useEffect(() => {
    if (map && maps) {
      if (circle) {
        circle.setOptions({center: props.center})
      }
      else {
        setCircle(new maps.Circle({
          strokeWeight: 0,
          fillColor: '#FF0000',
          fillOpacity: 0.2,
          map,
          center: props.center,
          radius: 5000,
        }));
      }
    }
  }, [props, map, maps]);

  // Important! Always set the container height explicitly
  return (
    <GoogleMap
      bootstrapURLKeys={{key: process.env.REACT_APP_GOOGLE_MAP_API}}
      center={props.center}
      zoom={12}
      onGoogleApiLoaded={({map, maps}) => {
        setMap(map);
        setMaps(maps);
      }}
    />
  )
};

export default SimpleMap;
