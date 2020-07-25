import React from 'react';
import Navbar from './components/Navigation/Navbar/Navbar'
import {BrowserRouter} from "react-router-dom";
import {ThemeProvider} from '@material-ui/core/styles';
import mainTheme from "./assets/styles/_theme";

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider theme={mainTheme}>
        <Navbar/>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
