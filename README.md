# Sander Kaatee - Interactive Recruiter Site

A modern, responsive one-page application designed to showcase Sander Kaatee's skills and experience to recruiters. Features an AI-powered chat interface, motivation letter, and CV viewer with Dutch/English language support.

## 🚀 Features

- **AI Chat Interface**: Real-time streaming chat powered by GPT-4o-mini with custom persona
- **Multilingual**: Full Dutch and English support with instant switching
- **Dark Mode**: Automatic theme detection with manual toggle
- **Mobile-First**: Fully responsive design optimized for all devices
- **Interactive UI**: Particle backgrounds, smooth animations, and glassmorphism design
- **WebSocket Communication**: Real-time bidirectional communication with fallback
- **Rate Limiting**: Redis-based rate limiting (5 requests/minute per IP)
- **Security**: HTTPS, comprehensive security headers, input validation
- **PDF Integration**: Embedded CV viewer with download capability

## 🛠 Tech Stack

### Frontend
- **SvelteKit 2.x** - Modern full-stack framework
- **TypeScript** - Type-safe development
- **TailwindCSS** - Utility-first CSS framework
- **Socket.IO Client** - Real-time WebSocket communication
- **TSParticles** - Interactive particle backgrounds
- **UUID** - Unique session identification

### Backend
- **Flask 3.x** - Lightweight Python web framework
- **Python 3.12** - Latest Python with async support
- **OpenAI API** - GPT-4o-mini for AI chat responses
- **Flask-SocketIO** - WebSocket server with eventlet
- **Redis** - In-memory data store for rate limiting
- **Gunicorn** - Production WSGI server

### Infrastructure
- **Docker & Docker Compose** - Containerized deployment
- **Caddy 2** - Automatic HTTPS and reverse proxy
- **Alpine Linux** - Lightweight container images

## 📋 Prerequisites

- Docker & Docker Compose
- OpenAI API key
- Domain with DNS pointing to your server (for production)
- Redis server (handled by Docker Compose)

## 🚀 Quick Start

### Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd sander-kaatee-recruiter-site
```

2. **Environment Configuration**
```bash
cp .env.sample .env
```

Edit `.env` with your configuration:
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key

# Application Settings
PUBLIC_WS_URL=ws://localhost:8001/ws/chat
PUBLIC_API_URL=http://localhost:8001/api
```

3. **Start Development Environment**
```bash
docker-compose up --build
```

4. **Access the Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- Health Check: http://localhost:8001/api/health

### Production Deployment

1. **Configure Production Environment**
```env
# Production URLs
PUBLIC_WS_URL=wss://your-domain.com/ws/chat
PUBLIC_API_URL=https://your-domain.com/api
OPENAI_API_KEY=sk-your-production-key
```

2. **Update Caddyfile**
```caddyfile
your-domain.com, www.your-domain.com {
    encode zstd gzip
    
    # WebSocket proxy
    @websocket {
        header Connection *Upgrade*
        header Upgrade websocket
    }
    reverse_proxy @websocket localhost:8001

    # API routes
    reverse_proxy /api/* localhost:8001
    
    # Frontend
    reverse_proxy localhost:3000
    
    # Security headers
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Frame-Options "DENY"
        X-Content-Type-Options "nosniff"
        X-XSS-Protection "1; mode=block"
        Referrer-Policy "strict-origin-when-cross-origin"
        Permissions-Policy "camera=(), microphone=(), geolocation=()"
    }
}
```

3. **Deploy**
```bash
docker-compose up -d --build
```

## 🏗 Architecture

### Frontend Structure
```
frontend/
├── src/
│   ├── lib/
│   │   ├── components/     # Reusable Svelte components
│   │   ├── stores/         # Global state management
│   │   └── types/          # TypeScript definitions
│   ├── routes/             # SvelteKit pages and API routes
│   └── app.html            # HTML template
├── static/                 # Static assets
└── tailwind.config.js      # Styling configuration
```

### Backend Structure
```
backend/
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── routes.py           # API endpoints and WebSocket handlers
│   ├── openai_client.py    # OpenAI API integration
│   ├── rate_limiter.py     # Redis-based rate limiting
│   └── config.py           # Application configuration
├── static/
│   └── profile_prompt.txt  # AI persona system prompt
└── requirements.txt        # Python dependencies
```

## 🤖 AI Chat Features

The AI chat interface includes:

- **Custom Persona**: Specialized AI assistant representing Sander Kaatee
- **Professional Context**: Deep knowledge of Sander's experience and skills
- **Rate Limiting**: 5 requests per minute per IP address
- **Real-time Streaming**: WebSocket-based communication
- **Error Handling**: Graceful fallbacks and user feedback
- **Conversation Continuity**: Maintains context throughout the chat

### Chat Commands
The AI can discuss:
- Sander's professional experience and skills
- Technical projects and achievements
- Career motivations and goals
- Specific questions about his background

## 🎨 Design Features

- **Glassmorphism UI**: Modern frosted glass aesthetic
- **Particle Backgrounds**: Interactive particle systems
- **Smooth Animations**: CSS transitions and transforms
- **Responsive Design**: Mobile-first approach
- **Accessibility**: WCAG-compliant color contrast and navigation
- **Performance**: Optimized images and lazy loading

## 🔒 Security Features

- **Rate Limiting**: Redis-based request throttling
- **Input Validation**: Server-side message sanitization
- **HTTPS Enforcement**: Automatic SSL/TLS with Caddy
- **Security Headers**: HSTS, CSP, and other protective headers
- **CORS Configuration**: Controlled cross-origin requests

## 📊 Monitoring & Health Checks

- **Health Endpoints**: `/healthz` and `/api/health`
- **Error Logging**: Comprehensive server-side logging
- **Rate Limit Monitoring**: Redis-based request tracking

## 🛠 Development

### Adding New Features

1. **Frontend Components**: Add to `frontend/src/lib/components/`
2. **Backend Routes**: Extend `backend/app/routes.py`
3. **Styling**: Use TailwindCSS utility classes
4. **State Management**: Utilize Svelte stores in `frontend/src/lib/stores/`

### Testing

```bash
# Frontend development
cd frontend && npm run dev

# Backend development
cd backend && python run.py

# Test WebSocket connection
cd backend && python test_client.py
```

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for chat functionality | Required |
| `PUBLIC_WS_URL` | WebSocket endpoint URL | `ws://localhost:8001/ws/chat` |
| `PUBLIC_API_URL` | API base URL | `http://localhost:8001/api` |
| `REDIS_URL` | Redis connection string | `redis://redis:6379` |

## 🚀 Deployment Options

### Docker Compose (Recommended)
Complete stack with automatic service orchestration

### Manual Deployment
1. Deploy backend with Gunicorn + eventlet
2. Build and serve frontend with Node.js
3. Configure Caddy for reverse proxy
4. Set up Redis for rate limiting

## 📄 License

Private project for recruitment purposes.

## 👤 Contact

**Sander Kaatee**
- Email: sanderkaatee@outlook.com
- Phone: +31-6-3433-2873
- LinkedIn: [linkedin.com/in/sander-kaatee](https://linkedin.com/in/sander-kaatee)
- GitHub: [github.com/SanderKaatee](https://github.com/SanderKaatee)

---

*Built with ❤️ using SvelteKit, Flask, and OpenAI*