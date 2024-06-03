import { Box, Button, Container, Input, Typography } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export function Settings() {
  const [saved, setSaved] = useState(false);
  const [splitwiseAPIKey, setSplitwiseAPIKey] = useState(
    localStorage.getItem("splitwiseAPIKey") || ""
  );
  const [toshlAPIKey, setToshlAPIKey] = useState(
    localStorage.getItem("toshlAPIKey") || ""
  );

  const navigate = useNavigate();
  const saveKeys = () => {
    if (saved) {
      navigate("/");
    } else {
      if (!splitwiseAPIKey || !toshlAPIKey) {
        alert("Please fill in both API keys.");
        return;
      }
      localStorage.setItem("splitwiseAPIKey", splitwiseAPIKey);
      localStorage.setItem("toshlAPIKey", toshlAPIKey);
      setSaved(true);
    }
  };
  return (
    <Container component="main" sx={{ mt: 8, mb: 2 }} maxWidth="sm">
      <Typography variant="h2" component="h1" gutterBottom>
        Settings
      </Typography>
      <Typography variant="h5" component="h2" gutterBottom>
        {"Configure your Splitwise and Toshl API keys."}
      </Typography>
      <Box sx={{ m: 2, display: "flex", flexDirection: "column", gap: 2 }}>
        <Input
          value={splitwiseAPIKey}
          onChange={(e) => {
            setSplitwiseAPIKey(e.target.value);
            setSaved(false);
          }}
          placeholder="Splitwise API Key"
          fullWidth
        />
        <Input
          value={toshlAPIKey}
          onChange={(e) => {
            setToshlAPIKey(e.target.value);
            setSaved(false);
          }}
          placeholder="Toshl API Key"
          fullWidth
        />
        <Button variant="contained" color="primary" onClick={saveKeys}>
          {saved ? "Done" : "Save"}
        </Button>
      </Box>
    </Container>
  );
}
