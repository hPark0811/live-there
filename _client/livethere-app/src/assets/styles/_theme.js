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
});

export default mainTheme;
