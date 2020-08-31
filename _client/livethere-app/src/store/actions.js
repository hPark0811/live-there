export const LOAD_UNIVERSITIES = 'LOAD_UNIVERSITIES';
export const SELECT_UNIVERSITY = 'SELECT_UNIVERSITY';

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
