import * as actionTypes from './actions.js';
import _ from "lodash"

const DEFAULT_SNACK_BAR_STATE = {
  show: false,
  message: null,
  duration: 10000,
  severity: "info" //error, warning, info, success
}

const initialState = {
  universityDict: {},
  selectedUniId: null,
  costOfLiving: {},
  snackBar: {...DEFAULT_SNACK_BAR_STATE}
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
    case actionTypes.SHOW_SNACK_BAR:
      return {
        ...state,
        snackBar: {
          ...DEFAULT_SNACK_BAR_STATE.snackBar,
          ...action.payload,
          show: true
        }
      }
    case actionTypes.HIDE_SNACK_BAR:
      return {
        ...state,
        snackBar: {...DEFAULT_SNACK_BAR_STATE}
      }
    default:
      return state;
  }
}
