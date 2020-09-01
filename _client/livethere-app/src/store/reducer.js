import * as actionTypes from './actions.js';
import _ from "lodash"

const initialState = {
  universityDict: {},
  selectedUniId: null,
  costOfLiving: {}
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
    case actionTypes.LOAD_COST_OF_LIVING_SUMMARY:
      const tempCostOfLivings = _.cloneDeep(state.costOfLiving);
      tempCostOfLivings[action.payload.label] = action.payload.estimate;
      return {
        ...state,
        costOfLiving: tempCostOfLivings
      }
    default:
      return state;
  }
}
