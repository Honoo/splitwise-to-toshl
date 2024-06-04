import express from "express";
import { createProxyMiddleware } from "http-proxy-middleware";

const app = express();

app.use(
  "/api/splitwise",
  createProxyMiddleware({
    target: "https://secure.splitwise.com/api",
    changeOrigin: true,
  })
);

app.use(
  "/api/toshl",
  createProxyMiddleware({
    target: "https://api.toshl.com/",
    changeOrigin: true,
  })
);

app.listen(5544);
