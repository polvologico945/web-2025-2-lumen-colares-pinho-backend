// index.js
import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

let posts = [
  { id: 1, title: "Post 1", body: "Conteúdo do post 1", user: "Carla Evelyn" },
  { id: 2, title: "Post 2", body: "Conteúdo do post 2", user: "Carla Evelyn" },
];

// Retorna todos os posts
app.get("/api/posts", (req, res) => {
  res.json(posts);
});

// Cria um novo post (apenas na memória)
app.post("/api/posts", (req, res) => {
  const { title, body, user } = req.body;
  const newPost = { id: posts.length + 1, title, body, user };
  posts.unshift(newPost);
  res.json(newPost);
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`Backend rodando em http://localhost:${PORT}`));
