import * as actionTypes from './actions.js'

const initialState = {
  universityDict: {},
  selectedUniId: null
}

export const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.LOAD_UNIVERSITIES:
      return {
        ...state,
        universityDict: action.payload.universityDict,
        selectedUniId: Object.keys(action.payload.universityDict)[0]
      }
    case actionTypes.SELECT_UNIVERSITY:
      return {
        ...state,
        selectedUniId: action.payload.selectedUniId
      }
    default:
      return state;
  }
}
