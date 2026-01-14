import express from "express";
import cors from "cors";
import { v4 as uuidv4 } from 'uuid';
import multer from 'multer';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

app.use(cors({
  origin: [
    'http://localhost:5173',
    'http://localhost:3000',
    'http://127.0.0.1:5173'
  ],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));

app.use(express.json());
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const uniqueName = `${Date.now()}-${file.originalname}`;
    cb(null, uniqueName);
  }
});

const upload = multer({
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|webp|gif/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (mimetype && extname) {
      return cb(null, true);
    } else {
      cb(new Error('Apenas imagens são permitidas'));
    }
  }
});

let usuarios = [];
let posts = [];
let noticias = [];
let comentarios = [];
let solicitacoes = [];

usuarios = [
  {
    id: uuidv4(),
    nome: "Carla Evelyn",
    email: "carlaevelyn@alu.ufc.br",
    senha: "senha123",
    username: "carla_e",
    avatar: "https://i.pravatar.cc/150?img=1",
    bio: "Estudante",
    papel: "admin"
  },
  {
    id: uuidv4(),
    nome: "Maria Barros",
    email: "maria.barros@alu.ufc.br",
    senha: "since2023",
    username: "maria_s",
    avatar: "https://i.pravatar.cc/150?img=2",
    bio: "Estudante",
    papel: "user"
  },
  {
    id: uuidv4(),
    nome: "Carla Evelyn",
    email: "carlaevelyn@alu.ufc.br",
    senha: "senha123",
    username: "carla_e2",
    avatar: "https://i.pravatar.cc/150?img=3",
    bio: "Estudante",
    papel: "user"
  },
  {
    id: uuidv4(),
    nome: "Francisco Robson Queiroz Mendes",
    email: "robsonqueirozmendes@gmail.com",
    senha: "password123",
    username: "robson_q",
    avatar: "https://i.pravatar.cc/150?img=4",
    bio: "Jovem dedicado e conservador, gosta de tecnologia e trabalha a 2 anos como desenvolvedor de software",
    papel: "user"
  },
  {
    id: uuidv4(),
    nome: "Pedro Nascimento",
    email: "pedro.nascimento@teste.com",
    senha: "pedropass",
    username: "pedro_n",
    avatar: "https://i.pravatar.cc/150?img=5",
    bio: "Analista",
    papel: "user"
  }
];

noticias = [
  {
    id: uuidv4(),
    titulo: "Horários de Ônibus Campus - Rodoviária",
    conteudo: "Confira os horários atualizados dos ônibus...",
    imagem: "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=600",
    autor: { nome: "Sistema" },
    categoria: "Serviços",
    dataPublicacao: new Date().toISOString(),
    visualizacoes: 342,
    curtidas: 45,
    comentarios: 18,
    destaque: true,
    horariosOnibus: [
      { viagem: 1, onibus: "A", saidaRodoviaria: "07h10", saidaCampus: "07h25" },
      { viagem: 2, onibus: "B", saidaRodoviaria: "07h15", saidaCampus: "07h30" },
      { viagem: 3, onibus: "A", saidaRodoviaria: "07h40", saidaCampus: "09h20" },
      { viagem: 4, onibus: "B", saidaRodoviaria: "07h45", saidaCampus: "11h10" },
      { viagem: 5, onibus: "A", saidaRodoviaria: "09h35", saidaCampus: "11h20" },
      { viagem: 6, onibus: "B", saidaRodoviaria: "11h25", saidaCampus: "11h40" },
      { viagem: 7, onibus: "A", saidaRodoviaria: "11h45", saidaCampus: "12h00" },
      { viagem: 8, onibus: "B", saidaRodoviaria: "12h05", saidaCampus: "12h20" },
      { viagem: 9, onibus: "A", saidaRodoviaria: "12h15", saidaCampus: "12h30" },
      { viagem: 10, onibus: "B", saidaRodoviaria: "12h35", saidaCampus: "12h50" },
      { viagem: 11, onibus: "A", saidaRodoviaria: "12h50", saidaCampus: "13h15" },
      { viagem: 12, onibus: "B", saidaRodoviaria: "13h05", saidaCampus: "15h15" },
      { viagem: 13, onibus: "A", saidaRodoviaria: "13h30", saidaCampus: "15h45" },
      { viagem: 14, onibus: "B", saidaRodoviaria: "15h30", saidaCampus: "17h20" },
      { viagem: 15, onibus: "A", saidaRodoviaria: "16h00", saidaCampus: "17h30" },
      { viagem: 16, onibus: "B", saidaRodoviaria: "17h35", saidaCampus: "17h50" },
      { viagem: 17, onibus: "A", saidaRodoviaria: "17h45", saidaCampus: "18h00" },
      { viagem: 18, onibus: "B", saidaRodoviaria: "18h05", saidaCampus: "18h20" },
      { viagem: 19, onibus: "A", saidaRodoviaria: "18h15", saidaCampus: "18h30" },
      { viagem: 20, onibus: "B", saidaRodoviaria: "18h35", saidaCampus: "22h10" },
      { viagem: 21, onibus: "A", saidaRodoviaria: "18h45", saidaCampus: "GARAGEM" }
    ]
  }
];

const autenticar = (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ 
      sucesso: false, 
      mensagem: "Token não fornecido" 
    });
  }
  
  req.usuarioId = 'usuario-autenticado';
  next();
};

app.get("/api/health", (req, res) => {
  res.json({ 
    sucesso: true,
    mensagem: "Backend Lumen Colares Online",
    timestamp: new Date().toISOString()
  });
});

app.post("/api/auth/login", (req, res) => {
  const { email, senha } = req.body;
  const user = usuarios.find(u => u.email === email && u.senha === senha);
  
  if (!user) {
    return res.status(401).json({ 
      sucesso: false, 
      mensagem: "Credenciais inválidas" 
    });
  }
  
  const token = `jwt-token-${user.id}`;
  const { senha: _, ...userSemSenha } = user;
  
  res.json({
    sucesso: true,
    mensagem: "Login realizado",
    token,
    usuario: userSemSenha
  });
});

app.get("/api/posts", (req, res) => {
  res.json({
    sucesso: true,
    quantidade: posts.length,
    dados: posts
  });
});

app.post("/api/posts", autenticar, upload.array('imagens', 5), (req, res) => {
  const { title, body, user } = req.body;
  
  const novoPost = {
    id: uuidv4(),
    title,
    body,
    user: user || "Anônimo",
    imagens: req.files ? req.files.map(f => `/uploads/${f.filename}`) : [],
    createdAt: new Date().toISOString(),
    likes: 0,
    comments: 0
  };
  
  posts.unshift(novoPost);
  res.status(201).json({
    sucesso: true,
    mensagem: "Post criado",
    dados: novoPost
  });
});

app.get("/api/noticias", (req, res) => {
  res.json({
    sucesso: true,
    quantidade: noticias.length,
    dados: noticias
  });
});

app.get("/api/noticias/onibus/horarios", (req, res) => {
  const noticiaOnibus = noticias.find(n => n.titulo.includes("Horários de Ônibus"));
  res.json({
    sucesso: true,
    dados: noticiaOnibus
  });
});

app.post("/api/solicitacoes", autenticar, (req, res) => {
  const { titulo, descricao } = req.body;
  
  const novaSolicitacao = {
    id: uuidv4(),
    titulo,
    descricao,
    usuarioId: req.usuarioId,
    status: 'pendente',
    dataCriacao: new Date().toISOString()
  };
  
  solicitacoes.push(novaSolicitacao);
  res.status(201).json({
    sucesso: true,
    mensagem: "Solicitação criada",
    dados: novaSolicitacao
  });
});

app.post("/api/posts/:id/comentarios", autenticar, (req, res) => {
  const { conteudo } = req.body;
  
  const novoComentario = {
    id: uuidv4(),
    postId: req.params.id,
    conteudo,
    autor: usuarios[0],
    data: new Date().toISOString()
  };
  
  comentarios.push(novoComentario);
  res.status(201).json({
    sucesso: true,
    mensagem: "Comentário adicionado",
    dados: novoComentario
  });
});

const PORT = process.env.PORT || 3001;
import fs from 'fs';
if (!fs.existsSync('uploads')) fs.mkdirSync('uploads');

app.listen(PORT, () => {
  console.log(`Backend rodando: http://localhost:${PORT}`);
});