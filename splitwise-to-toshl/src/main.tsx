import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import CssBaseline from "@mui/material/CssBaseline";
// import { createTheme, ThemeProvider } from "@mui/material/styles";
import Box from "@mui/material/Box";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ThemeProvider } from "@emotion/react";
import { createTheme } from "@mui/material";
import { Copyright } from "./Copyright.tsx";
import { Settings } from "./Settings.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/settings",
    element: <Settings />,
  },
  {
    path: "*",
    element: <div>Not Found</div>,
  },
]);

const defaultTheme = createTheme();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ThemeProvider theme={defaultTheme}>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          minHeight: "100vh",
        }}>
        <CssBaseline />

        <RouterProvider router={router} />

        <Box
          component="footer"
          sx={{
            py: 3,
            px: 2,
            mt: "auto",
            backgroundColor: (theme) =>
              theme.palette.mode === "light"
                ? theme.palette.grey[200]
                : theme.palette.grey[800],
          }}>
          <Container maxWidth="sm">
            <Typography variant="body1">
              Welcome to Splitwise to Toshl
            </Typography>
            <Copyright />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  </React.StrictMode>
);
