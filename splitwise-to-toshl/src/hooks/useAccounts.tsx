import React, {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
} from "react";

// Define the shape of your context state
type UserAccounts = {
  splitwise: {
    id: number;
    email: string;
  };
  toshl: {
    id: number;
    email: string;
  };
};

type UserAccountsContextType = {
  userAccounts: UserAccounts;
  accountsSet: boolean;
  loadUserAccounts: () => void;
};

// Create the context
const UserAccountsContext = createContext<UserAccountsContextType | undefined>(
  undefined
);

// Create a provider component
export const UserAccountsProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [userAccounts, setUserAccounts] = useState<UserAccounts>({
    splitwise: {
      id: 0,
      email: "",
    },
    toshl: {
      id: 0,
      email: "",
    },
  });

  const accountsSet = useMemo(() => {
    return userAccounts.splitwise.id !== 0 && userAccounts.toshl.id !== 0;
  }, [userAccounts]);

  const loadUserAccounts = useCallback(() => {
    const splitwiseAPIKey = localStorage.getItem("splitwiseAPIKey");
    const toshlAPIKey = localStorage.getItem("toshlAPIKey");

    if (splitwiseAPIKey && toshlAPIKey) {
      // setUserAccounts({
      //   splitwise: {
      //     id: 1,
      //     email: "",
      //   },
      //   toshl: {
      //     id: 1,
      //     email: "",
      //   },
      // });
    }
  }, []);

  const value = { userAccounts, loadUserAccounts, accountsSet };

  return (
    <UserAccountsContext.Provider value={value}>
      {children}
    </UserAccountsContext.Provider>
  );
};

// Create a custom hook to use the context
export const useUserAccounts = () => {
  const context = useContext(UserAccountsContext);
  if (context === undefined) {
    throw new Error(
      "useUserAccounts must be used within a UserAccountsProvider"
    );
  }
  return context;
};
