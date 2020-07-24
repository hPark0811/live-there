/* PLEASE REFER TO src/assets/styles/_breakpoints.scss for size reference */

import { useMediaQuery }from 'react-responsive'

const md = 960;

export const Desktop = ({ children }) => {
  const isDesktop = useMediaQuery({ minWidth: md })
  return isDesktop ? children : null
}

export const Mobile = ({ children }) => {
  const isMobile = useMediaQuery({ maxWidth: md - 1 })
  return isMobile ? children : null
}
