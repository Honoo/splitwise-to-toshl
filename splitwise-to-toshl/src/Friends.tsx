import { Box, Button, Container, styled, Typography } from "@mui/material";
import { useEffect, useState } from "react";

type SplitwiseFriend = {
  id: string;
  first_name: string;
  last_name: string;
  balance: {
    amount: number;
    currency_code: string;
  }[];
};

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
  const [friends, setFriends] = useState<SplitwiseFriend[]>([]);

  useEffect(() => {
    fetch("/api/splitwise/v3.0/get_friends", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("splitwiseAPIKey")}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        const friends = data.friends as SplitwiseFriend[];
        // sort by balance
        friends.sort((a, b) => {
          const aBalance = a.balance[0]?.amount || 0;
          const bBalance = b.balance[0]?.amount || 0;
          return bBalance - aBalance;
        });
        setFriends(friends);
      });
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
              {[friend.first_name, friend.last_name].filter(Boolean).join(", ")}
              {friend.balance[0]?.amount && friend.balance[0]?.amount > 0 && (
                <span
                  style={{
                    color: "grey",
                    marginLeft: "0.5rem",
                  }}>
                  (
                  {friend.balance
                    .map(
                      (balance) => `${balance.amount} ${balance.currency_code}`
                    )
                    .join(", ")}
                  )
                </span>
              )}
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
