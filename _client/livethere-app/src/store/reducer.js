import * as actionTypes from './actions.js'

const initialState = {
  universityDict: {}
}

export const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.LOAD_UNIVERSITIES:
      return {
        ...state,
        universityDict: action.payload.universityDict
      }
    default:
      return state;
  }
}
