import React from 'react';
import {BrowserRouter} from "react-router-dom";
import {ThemeProvider} from '@material-ui/core/styles';
import mainTheme from "./assets/styles/_theme";
import Layout from "./components/Layout/Layout";

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider theme={mainTheme}>
        <Layout/>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
