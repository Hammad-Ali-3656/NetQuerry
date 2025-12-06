# NetQuerry Deployment Guide

## Project Structure

Your app now has a multi-page structure:
- **Home.py** - Landing page with project introduction and YouTube video
- **pages/Chat_Interface.py** - Your original chat interface

## Running Locally

```bash
streamlit run Home.py
```

The app will open at `http://localhost:8501` with:
- Home page as the landing page
- Chat Interface accessible from sidebar or CTA button

## Deploying to Vercel (Recommended for Static Landing)

⚠️ **Important Note**: Vercel has limitations with Streamlit's interactive features. For full functionality, consider Streamlit Cloud instead.

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `Home.py`
   - Click "Deploy"

3. **Add YouTube Video**:
   - Once deployed, paste your YouTube URL in the text input
   - Video will embed automatically

**Benefits**:
- Free hosting
- Automatic updates from GitHub
- Full Streamlit functionality
- HTTPS by default
- No configuration needed

### Option 2: Heroku

1. **Install Heroku CLI**: [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Heroku App**:
   ```bash
   heroku create your-netquerry-app
   ```

4. **Deploy**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **Open App**:
   ```bash
   heroku open
   ```

### Option 3: Docker + Any Cloud Provider

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and Run**:
   ```bash
   docker build -t netquerry .
   docker run -p 8501:8501 netquerry
   ```

3. **Deploy to**:
   - Google Cloud Run
   - AWS ECS
   - Azure Container Apps
   - DigitalOcean App Platform

## Updating YouTube Video

### Method 1: Direct in App (After Deployment)
1. Visit your deployed app
2. Paste YouTube URL in the text input
3. Video embeds automatically

### Method 2: Hardcode URL (Before Deployment)

Edit `Home.py`, find this line:
```python
video_url = st.text_input(...)
```

Replace with:
```python
video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
st.markdown('<div class="video-container">', unsafe_allow_html=True)
st.video(video_url)
st.markdown('</div>', unsafe_allow_html=True)
```

## Environment Variables (Optional)

If you need to configure settings, create `.env`:
```bash
STREAMLIT_THEME=dark
DEFAULT_VIDEO_URL=https://www.youtube.com/watch?v=YOUR_VIDEO_ID
```

## Important Notes

1. **Database Files**: The `chroma*` directories are gitignored. Users will need to:
   - Add their own PDFs to `data/` folders
   - Let databases build on first query
   - Or pre-populate databases before deployment

2. **Ollama Dependency**: 
   - The chat interface requires Ollama running locally
   - For production, consider using cloud-based LLM APIs instead
   - Or deploy with Docker and include Ollama in the container

3. **File Storage**:
   - Streamlit Cloud has ephemeral storage
   - Databases will rebuild on each deployment
   - Consider using persistent storage (S3, Cloud Storage) for production

## Recommended Deployment Flow

1. **For Demo/Presentation**: Use Streamlit Cloud
   - Easiest and fastest
   - Free tier sufficient
   - Handles all Streamlit features perfectly

2. **For Production**: Use Docker on cloud provider
   - More control
   - Can bundle Ollama
   - Persistent storage options
   - Better performance

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Port already in use
```bash
streamlit run Home.py --server.port=8502
```

### Video not embedding
- Ensure URL is in format: `https://www.youtube.com/watch?v=VIDEO_ID`
- Or use short format: `https://youtu.be/VIDEO_ID`
- Check video is public (not private/unlisted)

### Pages not showing in sidebar
- Ensure `pages/` folder exists
- Files in `pages/` must end with `.py`
- Restart Streamlit app

## Quick Deploy Commands

```bash
# Local testing
streamlit run Home.py

# Streamlit Cloud (after GitHub push)
# Just visit share.streamlit.io and connect repo

# Heroku
heroku create your-app-name
git push heroku main

# Docker
docker build -t netquerry .
docker run -p 8501:8501 netquerry
```

## Support

For deployment issues:
- Streamlit Docs: [docs.streamlit.io](https://docs.streamlit.io)
- Streamlit Forum: [discuss.streamlit.io](https://discuss.streamlit.io)
- Heroku Docs: [devcenter.heroku.com](https://devcenter.heroku.com)
