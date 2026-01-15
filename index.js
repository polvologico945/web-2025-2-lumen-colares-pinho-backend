import 'dotenv/config'; 
import express from "express";
import cors from "cors";
import { v4 as uuidv4 } from 'uuid';
import multer from 'multer';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

app.use(cors({
  origin: [
    'http://localhost:5173',
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:5173'
  ],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));

app.use(express.json());
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Garantir que a pasta uploads existe
if (!fs.existsSync('uploads')) {
  fs.mkdirSync('uploads');
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const uniqueName = `${Date.now()}-${uuidv4()}-${file.originalname}`;
    cb(null, uniqueName);
  }
});

const upload = multer({
  storage: storage,
  limits: { 
    fileSize: 5 * 1024 * 1024, // 5MB
    files: 5 // Máximo de 5 arquivos
  },
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

// Dados em memória
let usuarios = [];
let posts = [];
let noticias = [];
let comentarios = [];

// Inicializar dados
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
      { viagem: 2, onibus: "B", saidaRodoviaria: "07h15", saidaCampus: "07h30" }
    ]
  }
];

// Middleware de autenticação
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

// Middleware de validação de post
const validarPost = (req, res, next) => {
  const { title, body } = req.body;
  const hasFiles = req.files && req.files.length > 0;
  
  // Se não tem arquivos, precisa ter conteúdo
  if (!hasFiles && (!title || !body || title.trim() === '' || body.trim() === '')) {
    return res.status(400).json({
      sucesso: false,
      mensagem: "Post deve conter texto ou pelo menos uma imagem"
    });
  }
  
  // Se tem conteúdo, validar mínimo
  if (body && body.trim().length < 1) {
    return res.status(400).json({
      sucesso: false,
      mensagem: "O conteúdo do post deve ter pelo menos 1 caractere"
    });
  }
  
  next();
};

// ROTAS
app.get("/api/health", (req, res) => {
  res.json({ 
    sucesso: true,
    mensagem: "Backend Lumen Online",
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

// ROTA POST ÚNICA E CORRETA
app.post("/api/posts", autenticar, (req, res, next) => {
  // Usar upload.array como middleware manualmente
  upload.array('imagens', 5)(req, res, function(err) {
    if (err instanceof multer.MulterError) {
      // Erros do multer
      if (err.code === 'LIMIT_FILE_SIZE') {
        return res.status(400).json({
          sucesso: false,
          mensagem: "Arquivo muito grande. Tamanho máximo: 5MB"
        });
      }
      if (err.code === 'LIMIT_FILE_COUNT') {
        return res.status(400).json({
          sucesso: false,
          mensagem: "Máximo de 5 imagens por post"
        });
      }
      if (err.code === 'LIMIT_UNEXPECTED_FILE') {
        return res.status(400).json({
          sucesso: false,
          mensagem: "Campo de upload deve ser 'imagens'"
        });
      }
      return res.status(400).json({
        sucesso: false,
        mensagem: `Erro no upload: ${err.message}`
      });
    } else if (err) {
      // Outros erros (ex: validação de tipo)
      return res.status(400).json({
        sucesso: false,
        mensagem: err.message
      });
    }
    
    // Validação manual do conteúdo
    const { title, body, user } = req.body;
    const hasContent = title && body && title.trim() !== '' && body.trim() !== '';
    const hasImages = req.files && req.files.length > 0;
    
    if (!hasContent && !hasImages) {
      return res.status(400).json({
        sucesso: false,
        mensagem: "Post deve conter texto ou pelo menos uma imagem"
      });
    }
    
    // Processar imagens
    const imagens = req.files ? req.files.map(f => `/uploads/${f.filename}`) : [];
    
    // Validar tipos de arquivo novamente
    const tiposPermitidos = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
    for (const file of req.files || []) {
      const ext = path.extname(file.originalname).toLowerCase();
      if (!tiposPermitidos.includes(ext)) {
        return res.status(400).json({
          sucesso: false,
          mensagem: `Arquivo ${file.originalname}: Tipo não permitido`
        });
      }
    }
    
    const novoPost = {
      id: uuidv4(),
      title: title || '',
      body: body || '',
      user: user || "Anônimo",
      imagens: imagens,
      createdAt: new Date().toISOString(),
      likes: 0,
      comments: 0,
      userId: req.usuarioId || 'usuario-autenticado'
    };
    
    posts.unshift(novoPost);
    
    res.status(201).json({
      sucesso: true,
      mensagem: "Post criado com sucesso",
      dados: novoPost
    });
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

// Rota para limites de upload (APENAS UMA)
app.get("/api/posts/upload-limits", (req, res) => {
  res.json({
    sucesso: true,
    limites: {
      max_imagens: 5,
      max_tamanho_mb: 5,
      tipos_permitidos: ['jpg', 'jpeg', 'png', 'gif', 'webp'],
      pasta_uploads: '/uploads'
    }
  });
});

app.put("/api/posts/:id", autenticar, (req, res, next) => {
  const postId = req.params.id;
  const { title, body, imagensParaRemover } = req.body;
  
  // Encontrar o post
  const postIndex = posts.findIndex(p => p.id === postId);
  if (postIndex === -1) {
    return res.status(404).json({
      sucesso: false,
      mensagem: "Post não encontrado"
    });
  }
  
  // Verificar autorização
  if (posts[postIndex].userId !== req.usuarioId) {
    return res.status(403).json({
      sucesso: false,
      mensagem: "Não autorizado"
    });
  }
  
  // Processar upload de novas imagens
  upload.array('imagens', 5)(req, res, function(err) {
    if (err) {
      return res.status(400).json({
        sucesso: false,
        mensagem: `Erro no upload: ${err.message}`
      });
    }
    
    const post = posts[postIndex];
    let imagensAtuais = post.imagens || [];
    
    // Remover imagens especificadas
    if (imagensParaRemover && Array.isArray(imagensParaRemover)) {
      imagensAtuais = imagensAtuais.filter(img => !imagensParaRemover.includes(img));
      
      // Deletar arquivos físicos
      imagensParaRemover.forEach(imgUrl => {
        if (imgUrl.startsWith('/uploads/')) {
          const filename = imgUrl.replace('/uploads/', '');
          const filepath = path.join(__dirname, 'uploads', filename);
          if (fs.existsSync(filepath)) {
            fs.unlinkSync(filepath);
          }
        }
      });
    }
    
    // Adicionar novas imagens
    const novasImagens = req.files ? req.files.map(f => `/uploads/${f.filename}`) : [];
    
    // VALIDAÇÃO: Máximo de 5 imagens no total
    const totalImagens = imagensAtuais.length + novasImagens.length;
    if (totalImagens > 5) {
      // Deletar arquivos recém-uploaded
      req.files?.forEach(file => {
        const filepath = path.join(__dirname, 'uploads', file.filename);
        if (fs.existsSync(filepath)) {
          fs.unlinkSync(filepath);
        }
      });
      
      return res.status(400).json({
        sucesso: false,
        mensagem: `Máximo de 5 imagens por post. Você já tem ${imagensAtuais.length} e tentou adicionar ${novasImagens.length}.`
      });
    }
    
    // Atualizar post
    posts[postIndex] = {
      ...post,
      title: title || post.title,
      body: body || post.body,
      imagens: [...imagensAtuais, ...novasImagens],
      updatedAt: new Date().toISOString()
    };
    
    res.json({
      sucesso: true,
      mensagem: "Post atualizado com sucesso",
      dados: posts[postIndex]
    });
  });
});

app.delete("/api/posts/:postId/imagens", autenticar, (req, res) => {
  const { postId } = req.params;
  const { imagemUrl } = req.body;
  
  const postIndex = posts.findIndex(p => p.id === postId);
  if (postIndex === -1) {
    return res.status(404).json({ sucesso: false, mensagem: "Post não encontrado" });
  }
  
  // Verificar autorização
  if (posts[postIndex].userId !== req.usuarioId) {
    return res.status(403).json({ sucesso: false, mensagem: "Não autorizado" });
  }
  
  // Remover imagem do array
  const post = posts[postIndex];
  if (!post.imagens || !post.imagens.includes(imagemUrl)) {
    return res.status(404).json({ sucesso: false, mensagem: "Imagem não encontrada no post" });
  }
  
  post.imagens = post.imagens.filter(img => img !== imagemUrl);
  
  // Deletar arquivo físico
  if (imagemUrl.startsWith('/uploads/')) {
    const filename = imagemUrl.replace('/uploads/', '');
    const filepath = path.join(__dirname, 'uploads', filename);
    if (fs.existsSync(filepath)) {
      fs.unlinkSync(filepath);
    }
  }
  
  res.json({
    sucesso: true,
    mensagem: "Imagem removida com sucesso",
    dados: post
  });
});

const PORT = process.env.PORT || 8000;

app.listen(PORT, () => {
  console.log(`Backend rodando: http://localhost:${PORT}`);
});