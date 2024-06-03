import { Box, Button, Container, styled, Typography } from "@mui/material";
import { useEffect, useState } from "react";

const FriendRow = styled(Box)`
  padding: 0.5rem;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  border: 1px solid #888;
`;
export function Friends() {
  const [friends, setFriends] = useState<unknown>([]);

  useEffect(() => {
    // fetch("https://secure.splitwise.com/api/v3.0/get_friends", {
    //   method: "GET",
    //   headers: {
    //     "Content-Type": "application/json",
    //     Authorization: `Bearer ${localStorage.getItem("splitwiseAPIKey")}`,
    //   },
    //   mode: "no-cors",
    // })
    //   .then((res) => res.json())
    //   .then((data) => {
    //     setFriends(data.friends);
    //   });
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append(
      "Authorization",
      "Bearer 1mgKsM1IJCQHuG1GozbS9kvTDfIDVw5rMCPO6SW5"
    );

    const requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow",
      mode: "no-cors",
    };

    fetch("https://secure.splitwise.com/api/v3.0/get_friends", requestOptions)
      .then((response) => response.text())
      .then((result) => console.log(result))
      .catch((error) => console.error(error));
  }, []);

  return (
    <Container component="main" sx={{ mt: 8, mb: 2 }} maxWidth="sm">
      <Typography variant="h2" component="h1" gutterBottom>
        Friends
      </Typography>
      <Typography variant="h5" component="h2" gutterBottom>
        {"Select who you want to transfer transactions for."}
      </Typography>
      <Box sx={{ p: 2, display: "flex", flexDirection: "column", gap: 1 }}>
        {friends.map((friend) => (
          <FriendRow key={friend.id}>
            <Typography variant="body1" component="p">
              {friend.first_name}
            </Typography>
            <Button
              variant="contained"
              color="primary"
              size="small"
              onClick={() => {}}>
              Next
            </Button>
          </FriendRow>
        ))}
      </Box>
    </Container>
  );
}
