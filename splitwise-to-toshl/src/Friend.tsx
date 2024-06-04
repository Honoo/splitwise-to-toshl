import { Box, Button, Container, Typography } from "@mui/material";
import { useEffect, useState } from "react";
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

const Expense = ({
  total,
  myShare,
  description,
}: {
  total: { amount: number; currency_code: string };
  myShare: { amount: number; currency_code: string };
  description: string;
}) => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        borderBottom: "1px solid #ccc",
        padding: "1rem",
      }}
    >
      <Box
        sx={{
          flexGrow: 1,
        }}
      >
        <Typography variant="h6" component="h3" align="left">
          {description}
        </Typography>
        <Typography variant="body2" component="h3" align="left">
          {description}
        </Typography>
      </Box>

      <Box>
        <Typography variant="body1" color="" align="right">
          Total: {total.amount} {total.currency_code}
        </Typography>
        <Typography variant="body1" color="primary" align="right">
          My Share: {myShare.amount} {myShare.currency_code}
        </Typography>
      </Box>
      <Button
        variant="contained"
        color="primary"
        sx={{
          marginLeft: "1rem",
        }}
      >
        Add
      </Button>
    </Box>
  );
};

export function Friend() {
  const { friendId } = useParams();
  const [friend, setFriend] = useState<SplitwiseFriend | null>(null);
  const [expenses, setExpenses] = useState<any[]>([]);
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (friendId === undefined) {
      return;
    }
    // Get friend details
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

    // Get expenses
    fetch(
      `/api/splitwise/v3.0/get_expenses?friend_id=${friendId}&limit=${count}&offset=${
        page * count
      }`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("splitwiseAPIKey")}`,
        },
      }
    )
      .then((res) => res.json())
      .then((data) => {
        setExpenses(data.expenses);
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
                }}
              >
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
          <Expense
            total={{
              amount: 1234,
              currency_code: "USD",
            }}
            myShare={{
              amount: 1234,
              currency_code: "USD",
            }}
            description="Item 1"
          />
          <Expense
            total={{
              amount: 1234,
              currency_code: "USD",
            }}
            myShare={{
              amount: 1234,
              currency_code: "USD",
            }}
            description="Item 1"
          />
          <Expense
            total={{
              amount: 1234,
              currency_code: "USD",
            }}
            myShare={{
              amount: 1234,
              currency_code: "USD",
            }}
            description="Item 1"
          />
        </Box>
      ) : (
        <Typography variant="h2" component="h1" gutterBottom>
          Loading...
        </Typography>
      )}
    </Container>
  );
}
