import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask settings
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)  # Reduced from 7 days for security
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'  # HTTPS only in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'  # More secure than Lax
    
    # Database
    DATABASE = 'gestao_empresarial.db'
    
    # AI Configuration
    AI_MIN_DADOS_PARA_ANALISE = 5  # Minimum number of sales for AI analysis
    AI_THRESHOLD_CRESCIMENTO = 0.10  # 10% growth threshold
    AI_THRESHOLD_QUEDA = 0.15  # 15% decline threshold
    AI_ESTOQUE_MINIMO_PERCENTUAL = 0.30  # 30% of average for low stock alert
    
    # Limits and constraints
    MAX_PRODUTOS_POR_USUARIO = 1000
    MAX_VENDAS_PAGINACAO = 50
    MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB
    
    # Report security
    RELATORIO_REQUERER_CONFIRMACAO_SENHA = True
    RELATORIO_TIMEOUT_MINUTOS = 15
    
    # Email configuration (optional, for future use)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Logging
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE = ':memory:'
    SESSION_COOKIE_SECURE = False

# Select configuration based on environment
def get_config():
    """Get configuration based on FLASK_ENV"""
    env = os.environ.get('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig
