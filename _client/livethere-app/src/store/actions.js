export const LOAD_UNIVERSITIES = 'LOAD_UNIVERSITIES';
export const SELECT_UNIVERSITY = 'SELECT_UNIVERSITY';
export const LOAD_COST_OF_LIVING_SUMMARY = 'LOAD_COST_OF_LIVING_SUMMARY';

export const loadUniversities = (payload) => {
  return {
    type: LOAD_UNIVERSITIES,
    payload
  }
}

export const selectUniversity = (payload) => {
  return {
    type: SELECT_UNIVERSITY,
    payload
  }
}

export const loadCostOfLivingSummary = (payload) => {
  return {
    type: LOAD_COST_OF_LIVING_SUMMARY,
    payload
  }
}
