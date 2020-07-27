import React from 'react';
import ReactDOM from 'react-dom';
import './index.scss';
import App from './app';
import * as serviceWorker from './serviceWorker';
import {createStore, applyMiddleware, compose} from "redux";
import {reducer} from "./store/reducer";
import {Provider} from "react-redux";
import thunk from "redux-thunk";

const middleware = store => {
  return (next) => {
    return (action) => {
      console.log('[Middleware] Dispatching', action);
      const result = next(action);

      console.log('[Middleware] Next state', store.getState());
      return result;
    }
  }
}

// Config to allow redux devtool usage
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(reducer, composeEnhancers(applyMiddleware(middleware, thunk)));

ReactDOM.render(
  <Provider store={store}>
    <React.StrictMode>
      <App/>
    </React.StrictMode>
  </Provider>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
