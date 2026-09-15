const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 80;

app.use(cors());
app.use(express.json());

const DB_DIR = path.join(__dirname, 'data');
const COMMUNITY_DB_FILE = path.join(DB_DIR, 'community_db.json');
const SEED_FILE = path.join(__dirname, 'site', 'data', 'community_seed.json');
const TIER_FILE = path.join(__dirname, 'site', 'data', 'tier_list_data.json');

// Ensure database files exist
if (!fs.existsSync(DB_DIR)) {
  fs.mkdirSync(DB_DIR, { recursive: true });
}

let communityPosts = [];
if (fs.existsSync(COMMUNITY_DB_FILE)) {
  try {
    communityPosts = JSON.parse(fs.readFileSync(COMMUNITY_DB_FILE, 'utf-8'));
  } catch(e) {
    communityPosts = [];
  }
}

if (!communityPosts.length && fs.existsSync(SEED_FILE)) {
  try {
    communityPosts = JSON.parse(fs.readFileSync(SEED_FILE, 'utf-8'));
    fs.writeFileSync(COMMUNITY_DB_FILE, JSON.stringify(communityPosts, null, 2));
  } catch(e) {}
}

let tierListData = [];
if (fs.existsSync(TIER_FILE)) {
  try {
    tierListData = JSON.parse(fs.readFileSync(TIER_FILE, 'utf-8'));
  } catch(e) {}
}

function saveCommunityDb() {
  try {
    fs.writeFileSync(COMMUNITY_DB_FILE, JSON.stringify(communityPosts, null, 2));
  } catch(e) {
    console.error('Error saving community db:', e);
  }
}

// ----------------------------------------------------
// COMMUNITY API ENDPOINTS
// ----------------------------------------------------

// 1. Get Community Posts
app.get('/api/community/posts', (req, res) => {
  const { category, sort } = req.query;
  let filtered = [...communityPosts];

  if (category && category !== 'all' && category !== 'todos') {
    filtered = filtered.filter(p => p.category === category);
  }

  if (sort === 'trending' || sort === 'alta') {
    filtered.sort((a, b) => (b.likes ? b.likes.length : 0) - (a.likes ? a.likes.length : 0));
  } else {
    filtered.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
  }

  res.json(filtered);
});

// 2. Create Community Post
app.post('/api/community/posts', (req, res) => {
  const { title, content, creatureSlug, category, author } = req.body;
  if (!title || !content || !author) {
    return res.status(400).json({ error: 'Título, conteúdo e autor são obrigatórios.' });
  }

  const newPost = {
    id: 'post_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5),
    author: {
      name: author.name || 'Inscrito DLuz',
      avatar: author.avatar || '/assets/dluz-logo.png',
      email: author.email || '',
      badge: author.badge || 'Inscrito VIP'
    },
    title: title.trim(),
    content: content.trim(),
    category: category || 'geral',
    creatureSlug: creatureSlug || null,
    createdAt: new Date().toISOString(),
    likes: [],
    comments: []
  };

  communityPosts.unshift(newPost);
  saveCommunityDb();
  res.status(201).json(newPost);
});

// 3. Toggle Like on Post
app.post('/api/community/posts/:id/like', (req, res) => {
  const { id } = req.params;
  const { userId } = req.body;
  if (!userId) return res.status(400).json({ error: 'userId obrigatório' });

  const post = communityPosts.find(p => p.id === id);
  if (!post) return res.status(404).json({ error: 'Post não encontrado' });

  post.likes = post.likes || [];
  const idx = post.likes.indexOf(userId);
  if (idx >= 0) {
    post.likes.splice(idx, 1);
  } else {
    post.likes.push(userId);
  }

  saveCommunityDb();
  res.json({ likesCount: post.likes.length, isLiked: idx === -1 });
});

// 4. Add Comment to Post
app.post('/api/community/posts/:id/comments', (req, res) => {
  const { id } = req.params;
  const { content, author } = req.body;
  if (!content || !author) return res.status(400).json({ error: 'Conteúdo e autor obrigatórios' });

  const post = communityPosts.find(p => p.id === id);
  if (!post) return res.status(404).json({ error: 'Post não encontrado' });

  post.comments = post.comments || [];
  const newComment = {
    id: 'c_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
    author: {
      name: author.name || 'Inscrito DLuz',
      avatar: author.avatar || '/assets/dluz-logo.png',
      badge: author.badge || 'Inscrito VIP'
    },
    content: content.trim(),
    createdAt: new Date().toISOString()
  };

  post.comments.push(newComment);
  saveCommunityDb();
  res.status(201).json(newComment);
});

function saveTierListDb() {
  try {
    const dbTierPath = path.join(DB_DIR, 'tier_list_data.json');
    fs.writeFileSync(dbTierPath, JSON.stringify(tierListData, null, 2));
    if (fs.existsSync(TIER_FILE)) {
      fs.writeFileSync(TIER_FILE, JSON.stringify(tierListData, null, 2));
    }
  } catch(e) {
    console.error('Error saving tier list db:', e);
  }
}

// ----------------------------------------------------
// TIER LIST VOTING API
// ----------------------------------------------------

app.get('/api/tier-list/votes', (req, res) => {
  res.json(tierListData);
});

app.post('/api/tier-list/vote', (req, res) => {
  const slug = req.body.slug || req.body.creatureSlug;
  const tier = req.body.tier;
  const note = req.body.note;
  const user = req.body.user || {};

  if (!slug || !tier) return res.status(400).json({ error: 'Dados inválidos' });

  const item = tierListData.find(c => c.slug === slug);
  if (item) {
    item.votes = item.votes || {};
    item.votes[tier] = (item.votes[tier] || 0) + 1;
    
    // Recalculate top tier
    let maxTier = tier;
    let maxVotes = 0;
    for (const [t, v] of Object.entries(item.votes)) {
      if (v > maxVotes) {
        maxVotes = v;
        maxTier = t;
      }
    }
    item.tier = maxTier;
    saveTierListDb();

    // If a note was left, add to community notes
    if (note && note.trim()) {
      communityPosts.unshift({
        id: 'note_' + Date.now(),
        author: {
          name: user.name || req.body.userName || 'Inscrito DLuz',
          avatar: user.avatar || req.body.userAvatar || '/assets/dluz-logo.png',
          badge: 'Voto na Tier List'
        },
        title: `Estratégia para ${item.name} (${tier})`,
        content: note.trim(),
        category: 'builds',
        creatureSlug: item.slug,
        createdAt: new Date().toISOString(),
        likes: [],
        comments: []
      });
      saveCommunityDb();
    }
  }

  res.json({ success: true, item, creature: item });
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', server: 'Aniimo DLuz Backend Engine', uptime: process.uptime() });
});

// Static files & SPA clean URL fallback
const SITE_DIR = path.join(__dirname, 'site');
app.use(express.static(SITE_DIR, { maxAge: '1d' }));

app.get('*', (req, res) => {
  // Check if specific sub-page html exists (e.g. /mapa/astra/index.html)
  const potentialFile = path.join(SITE_DIR, req.path, 'index.html');
  if (fs.existsSync(potentialFile)) {
    return res.sendFile(potentialFile);
  }
  res.sendFile(path.join(SITE_DIR, 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Aniimo DLuz Engine running on port ${PORT}`);
});
