# Adicione após as importações existentes
import os
from werkzeug.utils import secure_filename

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    likes = db.relationship('Like', back_populates='post', cascade='all, delete-orphan')
    
    # Adicione este campo para armazenar múltiplas imagens
    images = db.Column(db.JSON, default=list)  # Lista de URLs das imagens
    
    # Configurações para upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_IMAGES_PER_POST = 5
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'images': self.images if self.images else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'comments_count': len(self.comments) if self.comments else 0,
            'likes_count': len(self.likes) if self.likes else 0
        }
    
    # Método para validar arquivo
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Post.ALLOWED_EXTENSIONS
    
    # Método para validar imagem
    @staticmethod
    def validate_image(file):
        # Verificar se é um arquivo válido
        if not file or file.filename == '':
            return False, "Nenhum arquivo selecionado"
        
        # Verificar extensão
        if not Post.allowed_file(file.filename):
            return False, f"Tipo de arquivo não permitido. Tipos permitidos: {', '.join(Post.ALLOWED_EXTENSIONS)}"
        
        # Verificar tamanho do arquivo
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Voltar ao início do arquivo
        
        if file_size > Post.MAX_FILE_SIZE:
            return False, f"Arquivo muito grande. Tamanho máximo: {Post.MAX_FILE_SIZE // (1024*1024)}MB"
        
        return True, "OK"