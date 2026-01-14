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
    'http://127.0.0.1:5173',
    'https://web-2025-2-lumen-colares-pinho-frontend.vercel.app'
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
      cb(new Error('Apenas imagens são permitidas (JPEG, PNG, WebP, GIF)'));
    }
  }
});

let posts = [
  { 
    id: 1, 
    title: "Colar de Pérolas Artesanal", 
    body: "Colar feito com pérolas naturais e fio de seda", 
    user: "Carla Evelyn",
    price: 89.90,
    images: ["https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400"],
    createdAt: "2024-10-20T10:00:00Z",
    likes: 15,
    comments: 3
  },
  { 
    id: 2, 
    title: "Brinco de Prata 925", 
    body: "Brinco folheado a prata com cristais swarovski", 
    user: "Maria Silva",
    price: 45.50,
    images: ["https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400"],
    createdAt: "2024-10-19T14:30:00Z",
    likes: 8,
    comments: 1
  },
];

let noticias = [
  {
    id: uuidv4(),
    titulo: "Horários de Ônibus Campus - Rodoviária Atualizados",
    conteudo: `Confira os novos horários dos ônibus que fazem o trajeto entre a Rodoviária e o Campus UFC Quixadá. A tabela foi atualizada para melhor atender a comunidade acadêmica.

## Ônibus A e B em funcionamento:
- **Ônibus A**: Identificado com a letra A na tabela
- **Ônibus B**: Identificado com a letra B na tabela

## Informações:
- **Saída da Rodoviária**: Horário em que o ônibus parte da rodoviária
- **Saída do Campus**: Horário em que o ônibus parte do campus
- **GARAGEM**: Ônibus retorna à garagem após o horário

## Tabela Completa de Horários:`,
    imagem: "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=600",
    autor: {
      id: 1,
      nome: "Transporte Universitário",
      avatar: "https://i.pravatar.cc/150?img=10"
    },
    categoria: "Serviços",
    tags: ["transporte", "ônibus", "horários", "campus", "rodoviária"],
    dataPublicacao: "2024-10-20T08:00:00Z",
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
  },
  {
    id: uuidv4(),
    titulo: "Workshop de Artesanato Digital - Inscrições Abertas",
    conteudo: "Participe do nosso workshop gratuito sobre como vender artesanato online. Aprenda técnicas de fotografia, precificação e marketing digital.",
    imagem: "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=600",
    autor: {
      id: 2,
      nome: "Carla Evelyn",
      avatar: "https://i.pravatar.cc/150?img=1"
    },
    categoria: "Eventos",
    tags: ["artesanato", "workshop", "digital", "vendas"],
    dataPublicacao: "2024-10-18T09:00:00Z",
    visualizacoes: 156,
    curtidas: 34,
    comentarios: 12,
    destaque: true
  },
  {
    id: uuidv4(),
    titulo: "Nova Coleção de Colares de Outono",
    conteudo: "Acabamos de lançar nossa coleção de outono com pedras naturais e tons terrosos. Cada peça é feita manualmente com materiais sustentáveis.",
    imagem: "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600",
    autor: {
      id: 3,
      nome: "Maria Silva",
      avatar: "https://i.pravatar.cc/150?img=2"
    },
    categoria: "Novidades",
    tags: ["coleção", "outono", "sustentável", "lançamento"],
    dataPublicacao: "2024-10-15T14:30:00Z",
    visualizacoes: 234,
    curtidas: 78,
    comentarios: 21,
    destaque: true
  },
  {
    id: uuidv4(),
    titulo: "Feira de Artesanato Universitário",
    conteudo: "Venha conferir a feira de artesanato organizada pelos alunos. Produtos exclusivos e preços especiais para a comunidade acadêmica.",
    imagem: "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=600",
    autor: {
      id: 4,
      nome: "Coordenação de Eventos",
      avatar: "https://i.pravatar.cc/150?img=4"
    },
    categoria: "Eventos",
    tags: ["feira", "artesanato", "universitário", "evento"],
    dataPublicacao: "2024-10-12T11:15:00Z",
    visualizacoes: 189,
    curtidas: 56,
    comentarios: 8,
    destaque: false
  }
];

let usuarios = [
  {
    id: 2,
    nome: "Maria Barros",
    email: "maria.barros@alu.ufc.br",
    senha: "since2023",
    username: "maria_barros",
    avatar: "https://i.pravatar.cc/150?img=2",
    bio: "Estudante"
  }
];

const autenticar = (req, res, next) => {
  const token = req.headers.authorization;
  
  if (!token || !token.includes('jwt-token')) {
    return res.status(401).json({ 
      sucesso: false, 
      mensagem: "Token inválido ou não fornecido" 
    });
  }
  
  req.usuarioId = 1;
  req.usuarioNome = "Usuário Autenticado";
  next();
};

app.get("/api/health", (req, res) => {
  res.json({ 
    sucesso: true,
    mensagem: "Backend Lumen Colares & Pinho Online",
    timestamp: new Date().toISOString(),
    versao: "1.0.0",
    estatisticas: {
      posts: posts.length,
      noticias: noticias.length,
      usuarios: usuarios.length
    }
  });
});

app.get("/api/posts", (req, res) => {
  res.json({
    sucesso: true,
    quantidade: posts.length,
    dados: posts
  });
});

app.get("/api/posts/:id", (req, res) => {
  const post = posts.find(p => p.id === parseInt(req.params.id));
  if (!post) return res.status(404).json({ 
    sucesso: false, 
    mensagem: "Post não encontrado" 
  });
  res.json({
    sucesso: true,
    dados: post
  });
});

app.post("/api/posts", autenticar, upload.array('imagens', 5), (req, res) => {
  const { title, body, user, price } = req.body;
  
  if (!title || !body) {
    return res.status(400).json({ 
      sucesso: false, 
      mensagem: "Título e conteúdo são obrigatórios" 
    });
  }
  
  const imagens = req.files ? req.files.map(file => ({
    url: `/uploads/${file.filename}`,
    nome: file.originalname,
    tamanho: file.size,
    tipo: file.mimetype
  })) : [];
  
  if (imagens.length > 5) {
    return res.status(400).json({
      sucesso: false,
      mensagem: "Máximo de 5 imagens por post"
    });
  }
  
  const newPost = { 
    id: posts.length + 1, 
    title, 
    body, 
    user: user || "Anônimo",
    price: price || 0,
    images: imagens,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    likes: 0,
    comments: 0
  };
  
  posts.unshift(newPost);
  
  res.status(201).json({
    sucesso: true,
    mensagem: "Post criado com sucesso",
    dados: newPost
  });
});

app.put("/api/posts/:id", autenticar, (req, res) => {
  const { title, body, price } = req.body;
  const postIndex = posts.findIndex(p => p.id === parseInt(req.params.id));
  
  if (postIndex === -1) {
    return res.status(404).json({ 
      sucesso: false, 
      mensagem: "Post não encontrado" 
    });
  }
  
  posts[postIndex] = {
    ...posts[postIndex],
    title: title || posts[postIndex].title,
    body: body || posts[postIndex].body,
    price: price || posts[postIndex].price,
    updatedAt: new Date().toISOString()
  };
  
  res.json({
    sucesso: true,
    mensagem: "Post atualizado com sucesso",
    dados: posts[postIndex]
  });
});

app.delete("/api/posts/:id", autenticar, (req, res) => {
  const initialLength = posts.length;
  posts = posts.filter(p => p.id !== parseInt(req.params.id));
  
  if (posts.length === initialLength) {
    return res.status(404).json({ 
      sucesso: false, 
      mensagem: "Post não encontrado" 
    });
  }
  
  res.json({
    sucesso: true,
    mensagem: "Post deletado com sucesso"
  });
});

app.get("/api/noticias", (req, res) => {
  const { categoria, destaque, limit } = req.query;
  
  let noticiasFiltradas = [...noticias];
  
  if (categoria) {
    noticiasFiltradas = noticiasFiltradas.filter(n => 
      n.categoria.toLowerCase() === categoria.toLowerCase()
    );
  }
  
  if (destaque === "true") {
    noticiasFiltradas = noticiasFiltradas.filter(n => n.destaque);
  }
  
  noticiasFiltradas.sort((a, b) => 
    new Date(b.dataPublicacao) - new Date(a.dataPublicacao)
  );
  
  if (limit) {
    noticiasFiltradas = noticiasFiltradas.slice(0, parseInt(limit));
  }
  
  res.json({
    sucesso: true,
    quantidade: noticiasFiltradas.length,
    dados: noticiasFiltradas
  });
});

app.get("/api/noticias/:id", (req, res) => {
  const noticia = noticias.find(n => n.id === req.params.id);
  
  if (!noticia) {
    return res.status(404).json({ 
      sucesso: false, 
      mensagem: "Notícia não encontrada" 
    });
  }
  
  noticia.visualizacoes += 1;
  
  res.json({
    sucesso: true,
    dados: noticia
  });
});

app.get("/api/noticias/onibus/horarios", (req, res) => {
  const noticiaOnibus = noticias.find(n => 
    n.titulo.includes("Horários de Ônibus")
  );
  
  if (!noticiaOnibus) {
    return res.status(404).json({
      sucesso: false,
      mensagem: "Notícia sobre horários de ônibus não encontrada"
    });
  }
  
  noticiaOnibus.visualizacoes += 1;
  
  res.json({
    sucesso: true,
    dados: {
      titulo: noticiaOnibus.titulo,
      conteudo: noticiaOnibus.conteudo,
      horarios: noticiaOnibus.horariosOnibus,
      ultimaAtualizacao: noticiaOnibus.dataPublicacao
    }
  });
});

app.get("/api/onibus/:tipo", (req, res) => {
  const { tipo } = req.params;
  const noticiaOnibus = noticias.find(n => 
    n.titulo.includes("Horários de Ônibus")
  );
  
  if (!noticiaOnibus) {
    return res.status(404).json({
      sucesso: false,
      mensagem: "Dados de ônibus não encontrados"
    });
  }
  
  const horariosFiltrados = noticiaOnibus.horariosOnibus.filter(
    h => h.onibus === tipo.toUpperCase()
  );
  
  res.json({
    sucesso: true,
    onibus: tipo.toUpperCase(),
    quantidade: horariosFiltrados.length,
    dados: horariosFiltrados
  });
});

app.post("/api/noticias", autenticar, (req, res) => {
  const { titulo, conteudo, imagem, categoria, tags } = req.body;
  
  if (!titulo || !conteudo) {
    return res.status(400).json({
      sucesso: false,
      mensagem: "Título e conteúdo são obrigatórios"
    });
  }
  
  const novaNoticia = {
    id: uuidv4(),
    titulo,
    conteudo,
    imagem: imagem || "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=600",
    autor: {
      id: req.usuarioId,
      nome: req.usuarioNome,
      avatar: "https://i.pravatar.cc/150?img=5"
    },
    categoria: categoria || "Geral",
    tags: tags || [],
    dataPublicacao: new Date().toISOString(),
    visualizacoes: 0,
    curtidas: 0,
    comentarios: 0,
    destaque: false
  };
  
  noticias.unshift(novaNoticia);
  
  res.status(201).json({
    sucesso: true,
    mensagem: "Notícia criada com sucesso",
    dados: novaNoticia
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
  
  const token = `jwt-token-${user.id}-${Date.now()}`;
  
  const { senha: _, ...userSemSenha } = user;
  
  res.json({
    sucesso: true,
    mensagem: "Login realizado com sucesso",
    token,
    usuario: userSemSenha
  });
});

app.get("/api/auth/me", autenticar, (req, res) => {
  const user = usuarios.find(u => u.id === req.usuarioId);
  
  if (!user) {
    return res.status(404).json({
      sucesso: false,
      mensagem: "Usuário não encontrado"
    });
  }
  
  const { senha: _, ...userSemSenha } = user;
  
  res.json({
    sucesso: true,
    dados: userSemSenha
  });
});

let comentarios = [];

app.get("/api/posts/:id/comentarios", (req, res) => {
  const postComentarios = comentarios.filter(c => c.postId === parseInt(req.params.id));
  
  res.json({
    sucesso: true,
    quantidade: postComentarios.length,
    dados: postComentarios.sort((a, b) => new Date(b.data) - new Date(a.data))
  });
});

app.post("/api/posts/:id/comentarios", autenticar, (req, res) => {
  const { conteudo } = req.body;
  
  if (!conteudo || conteudo.trim() === '') {
    return res.status(400).json({
      sucesso: false,
      mensagem: "Conteúdo do comentário é obrigatório"
    });
  }
  
  const novoComentario = {
    id: uuidv4(),
    postId: parseInt(req.params.id),
    conteudo,
    autor: {
      id: req.usuarioId,
      nome: req.usuarioNome,
      avatar: "https://i.pravatar.cc/150?img=1"
    },
    data: new Date().toISOString(),
    curtidas: 0
  };
  
  comentarios.push(novoComentario);
  
  const postIndex = posts.findIndex(p => p.id === parseInt(req.params.id));
  if (postIndex !== -1) {
    posts[postIndex].comments += 1;
  }
  
  res.status(201).json({
    sucesso: true,
    mensagem: "Comentário adicionado com sucesso",
    dados: novoComentario
  });
});

let solicitacoes = [];

app.post("/api/solicitacoes", autenticar, (req, res) => {
  const { titulo, descricao } = req.body;
  
  const novaSolicitacao = {
    id: uuidv4(),
    titulo,
    descricao,
    usuarioId: req.usuarioId,
    status: 'pendente',
    dataCriacao: new Date().toISOString(),
    dataAtualizacao: new Date().toISOString()
  };
  
  solicitacoes.push(novaSolicitacao);
  
  res.status(201).json({
    sucesso: true,
    mensagem: "Solicitação criada com sucesso",
    dados: novaSolicitacao
  });
});

app.get("/api/solicitacoes/minhas", autenticar, (req, res) => {
  const minhasSolicitacoes = solicitacoes.filter(s => s.usuarioId === req.usuarioId);
  
  res.json({
    sucesso: true,
    quantidade: minhasSolicitacoes.length,
    dados: minhasSolicitacoes
  });
});

const PORT = process.env.PORT || 3001;

import fs from 'fs';
if (!fs.existsSync('uploads')) {
  fs.mkdirSync('uploads');
}

app.listen(PORT, () => {
  console.log(`
BACKEND LUMEN COLARES & PINHO
URL: http://localhost:${PORT}

ENDPOINTS DISPONÍVEIS:

AUTENTICAÇÃO:
   POST /api/auth/login
   GET  /api/auth/me (protegido)

POSTS (CRUD com upload de imagens):
   GET    /api/posts
   GET    /api/posts/:id
   POST   /api/posts           (upload de até 5 imagens)
   PUT    /api/posts/:id
   DELETE /api/posts/:id

NOTÍCIAS (com horários de ônibus):
   GET /api/noticias
   GET /api/noticias/:id
   GET /api/noticias/onibus/horarios
   GET /api/onibus/:tipo        (A ou B)
   POST /api/noticias (protegido)

INTERAÇÕES:
   GET  /api/posts/:id/comentarios
   POST /api/posts/:id/comentarios

FLUXO TRANSAÇÃO (opcional):
   POST /api/solicitacoes
   GET  /api/solicitacoes/minhas

SAÚDE:
   GET /api/health

UPLOADS: http://localhost:${PORT}/uploads
`);
});