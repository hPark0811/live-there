import {createMuiTheme} from '@material-ui/core/styles';

const mainTheme = createMuiTheme({
  palette: {
    primary: {
      light: '#33c9dc',
      main: '#00bcd4',
      dark: '#008394',
      contrastText: '#fff',
    },
    secondary: {
      light: '#b23939',
      main: '#ff5252',
      dark: '#ff7474',
      contrastText: '#fff',
    },
  },
  /* // Default zIndex set by Material-UI
  * zIndex = {
      mobileStepper: 1000,
      speedDial: 1050,
      appBar: 1100,
      drawer: 1200,
      modal: 1300,
      snackbar: 1400,
      tooltip: 1500,
  };
  * */
  typography: {
    fontFamily: 'open-sans',
    fontSize: 12,
    h1: {
      fontWeight: 'bold',
      fontSize: '2.6rem',
      '@media (min-width: 960px)': {
        fontSize: '4rem',
      }
    },
    h2: {
      fontSize: '1.8rem',
      '@media (min-width: 960px)': {
        fontSize: '2.8rem',
      }
    },
    h3: {
      fontSize: '1.4rem',
      '@media (min-width: 960px)': {
        fontSize: '2.6rem',
      }
    },
    h4: {
      fontSize: '1.2rem',
      '@media (min-width: 960px)': {
        fontSize: '1.8rem',
      }
    },
    h5: {
      fontSize: '1rem',
      '@media (min-width: 960px)': {
        fontSize: '1.5rem',
      }
    },
    subtitle1: {
      fontSize: '0.8rem',
      lineHeight: 1.4,
      '@media (min-width: 960px)': {
        fontSize: '1rem',
      }
    }
  }
});

export default mainTheme;
