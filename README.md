# Sander Kaatee - Recruiter Site

A modern, responsive one-page application designed to showcase Sander Kaatee's skills and experience to recruiters. Features an AI-powered chat interface, motivation letter, and CV viewer with Dutch/English language support.

## 🚀 Features

- **AI Chat Interface**: Real-time streaming chat powered by GPT-4o-mini
- **Multilingual**: Full Dutch and English support with instant switching
- **Dark Mode**: Automatic theme detection with manual toggle
- **Mobile-First**: Fully responsive design optimized for all devices
- **Glassmorphism UI**: Modern, clean aesthetic inspired by chat4data.ai
- **WebSocket Communication**: Real-time bidirectional communication
- **Rate Limiting**: Redis-based rate limiting (5 requests/minute)
- **Security**: HTTPS, security headers, input validation

## 🛠 Tech Stack

- **Frontend**: SvelteKit 2.x, TailwindCSS, TypeScript
- **Backend**: Flask 3.x, Python 3.12, OpenAI API
- **WebSocket**: Flask-SocketIO with async support
- **Database**: Redis for rate limiting
- **Deployment**: Docker, Docker Compose, Caddy

## 📋 Prerequisites

- Docker & Docker Compose
- OpenAI API key
- Domain with DNS pointing to your server
- Hetzner VPS (or similar) with Caddy installed

## 🚀 Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sander-kaatee-hire.git
cd sander-kaatee-hire
```

2. Copy environment variables:
```bash
cp .env.sample .env
```

3. Edit `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

4. Start the application:
```bash
docker compose up -d --build
```

5. Open http://localhost:3000

### Production Deployment

1. SSH into your VPS:
```bash
ssh root@your-server-ip
```

2. Clone the repository:
```bash
cd /srv
git clone https://github.com/yourusername/sander-kaatee-hire.git
cd sander-kaatee-hire
```

3. Create production environment file:
```bash
cp .env.sample .env
nano .env  # Add your OPENAI_API_KEY and update URLs
```

4. Update the Caddyfile:
```bash
sudo nano /etc/caddy/Caddyfile
```

Add the configuration from the project's Caddyfile, then:
```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

5. Start the application:
```bash
docker compose up -d --build
```

6. Verify deployment:
```bash
docker compose ps
curl http://localhost:3000/api/health
```

## 📁 Project Structure

```
├── frontend/          # SvelteKit application
│   ├── src/
│   │   ├── lib/       # Components, stores, i18n
│   │   ├── routes/    # Page routes
│   │   └── app.css    # Global styles
│   └── static/        # Static assets (CV PDF)
├── backend/           # Flask application
│   ├── app/           # Application modules
│   └── static/        # Profile data (YAML)
├── docker-compose.yml # Container orchestration
├── Caddyfile         # Reverse proxy config
└── .env.sample       # Environment template
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `PUBLIC_WS_URL` | WebSocket URL | `wss://hire.smeister.xyz/ws/chat` |
| `PUBLIC_API_URL` | API base URL | `https://hire.smeister.xyz/api` |

### Customization

1. **Profile Data**: Edit `backend/static/profile.yaml`
2. **CV**: Replace `frontend/static/cv.pdf`
3. **Translations**: Update `frontend/src/lib/i18n/[en|nl].json`
4. **Colors**: Modify `frontend/tailwind.config.js`

## 🚨 Monitoring

### Health Checks
- Frontend: `GET /api/health`
- Backend: `GET /healthz`

### Logs
```bash
# View all logs
docker compose logs -f

# Specific service
docker compose logs -f backend
```

### Container Status
```bash
docker compose ps
```

## 🔒 Security

- Rate limiting: 5 requests/minute per IP
- Input validation and sanitization
- Security headers via Caddy
- No conversation data stored
- HTTPS enforced in production

## 📝 Development

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python -m flask run
```

## 🐛 Troubleshooting

### WebSocket Connection Issues
- Check if backend is running: `docker compose ps`
- Verify WebSocket URL in `.env`
- Check browser console for errors

### Rate Limiting
- Redis must be running
- Check Redis connection in logs

### Chat Not Working
- Verify OpenAI API key
- Check backend logs for errors
- Ensure sufficient API credits

## 📄 License

MIT License - feel free to use this project as a template for your own portfolio.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

**SHA-256**: `[Generated after final commit]`

Built with ❤️ using SvelteKit, Flask, and Docker