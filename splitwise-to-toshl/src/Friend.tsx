import { Box, Container, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export type SplitwiseFriend = {
  id: string;
  first_name: string;
  last_name: string;
  balance: {
    amount: number;
    currency_code: string;
  }[];
};

export function Friend() {
  const { friendId } = useParams();
  const [friend, setFriend] = useState<SplitwiseFriend | null>(null);

  useEffect(() => {
    if (friendId === undefined) {
      return;
    }
    fetch(`/api/splitwise/v3.0/get_friend/${friendId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("splitwiseAPIKey")}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setFriend(data.friend as SplitwiseFriend);
      });
  }, [friendId]);

  return (
    <Container component="main" sx={{ mt: 8, mb: 2 }} maxWidth="sm">
      {friend ? (
        <Box>
          <Typography variant="h2" component="h1">
            {[friend.first_name, friend.last_name].filter(Boolean).join(", ")}
          </Typography>
          <Typography variant="h5" component="h2" gutterBottom>
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
        </Box>
      ) : (
        <Typography variant="h2" component="h1" gutterBottom>
          Loading...
        </Typography>
      )}
    </Container>
  );
}
