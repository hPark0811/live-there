import {useEffect, useRef} from "react";

const useIsMountedRef = () => {
  const isMountedRef = useRef(false);
  useEffect(() => {
    isMountedRef.current = true;
    return () => isMountedRef.current = false;
  });
  return isMountedRef;
}

export default useIsMountedRef;
