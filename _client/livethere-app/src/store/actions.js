export const LOAD_UNIVERSITIES = 'LOAD_UNIVERSITIES';

export const loadUniversities = (payload) => {
  return {
    type: LOAD_UNIVERSITIES,
    payload
  }
}
