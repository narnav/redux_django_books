import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "../features/counter/counterSlice";
import bookReducer from "./bookSlice";
import loginReducer from "./loginSlice";
import noteReducer from "./noteSlice";

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    login: loginReducer,
    note: noteReducer,
    book: bookReducer,
  },
});
