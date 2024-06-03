import "./App.css";

import Typography from "@mui/material/Typography";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Container } from "@mui/material";

function App() {
  const splitwiseAPIKey = localStorage.getItem("splitwiseAPIKey");
  const toshlAPIKey = localStorage.getItem("toshlAPIKey");

  const navigate = useNavigate();

  useEffect(() => {
    if (!splitwiseAPIKey || !toshlAPIKey) {
      navigate("/settings");
    }
  }, [navigate, splitwiseAPIKey, toshlAPIKey]);

  const last5Characters = (str: string | null) => {
    if (!str) {
      return "null";
    }
    return `****${str.slice(-5)}`;
  };

  return (
    <Container component="main" sx={{ mt: 8, mb: 2 }} maxWidth="sm">
      <Typography variant="h2" component="h1" gutterBottom>
        Splitwise to Toshl
      </Typography>

      <Box
        sx={{
          position: "absolute",
          top: "10px",
          right: "10px",
        }}>
        <Typography
          variant="body1"
          component="p"
          sx={{
            textAlign: "right",
          }}
          gutterBottom>
          <div>API Keys:</div>
          <div>Splitwise: {last5Characters(splitwiseAPIKey)}</div>
          <div>Toshl: {last5Characters(toshlAPIKey)}</div>
          <a href="/settings">Settings</a>
        </Typography>
      </Box>
      <Typography variant="h5" component="h2" gutterBottom>
        {"Pin a footer to the bottom of the viewport."}
        {"The footer will move as the main element of the page grows."}
      </Typography>
      <Typography variant="body1">Sticky footer placeholder.</Typography>
    </Container>
  );
}

export default App;
