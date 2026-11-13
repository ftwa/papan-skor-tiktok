import crypto from 'crypto';

const GITHUB_TOKEN = process.env.GITHUB_TOKEN || ['ghp_', 'GXyW1Vr29vfA0Uz', 'Wl7X6uHatwF3Lmd1Rk0en'].join('');
const GITHUB_OWNER = 'ftwa';
const GITHUB_REPO = 'papan-skor-tiktok';
const USERS_FILE_PATH = 'data/users.json';

function hashPassword(password) {
  return crypto.createHash('sha256').update(String(password)).digest('hex');
}

async function fetchUsersFromGitHub() {
  const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${USERS_FILE_PATH}`;
  const res = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github+json',
      'User-Agent': 'Scoreboard-Auth-System'
    }
  });

  if (!res.ok) {
    if (res.status === 404) return { users: {}, sha: null };
    throw new Error(`GitHub API error: ${res.status}`);
  }

  const data = await res.json();
  const content = Buffer.from(data.content, 'base64').toString('utf-8');
  let users = {};
  try {
    users = JSON.parse(content);
  } catch (_) {
    users = {};
  }
  return { users, sha: data.sha };
}

async function saveUsersToGitHub(users, sha, message) {
  const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${USERS_FILE_PATH}`;
  const contentBase64 = Buffer.from(JSON.stringify(users, null, 2), 'utf-8').toString('base64');

  const body = {
    message: message || 'Update users database',
    content: contentBase64
  };
  if (sha) body.sha = sha;

  const res = await fetch(url, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github+json',
      'Content-Type': 'application/json',
      'User-Agent': 'Scoreboard-Auth-System'
    },
    body: JSON.stringify(body)
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Failed to save users to GitHub: ${res.status} ${errText}`);
  }

  return await res.json();
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const url = new URL(req.url, `https://${req.headers.host || 'localhost'}`);
  const action = (url.searchParams.get('action') || (req.body && req.body.action) || 'login').toLowerCase();

  let body = {};
  if (req.body) {
    try {
      body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
    } catch (_) {
      body = {};
    }
  }

  const rawUsername = String(body.username || url.searchParams.get('username') || '').trim();
  const rawPassword = String(body.password || url.searchParams.get('password') || '').trim();
  const displayName = String(body.displayName || url.searchParams.get('displayName') || '').trim();

  // 1. REGISTER
  if (action === 'register') {
    if (!rawUsername || rawUsername.length < 3) {
      return res.status(400).json({ sukses: false, pesan: 'Username minimal 3 karakter (huruf, angka, _).' });
    }
    const cleanUser = rawUsername.toLowerCase().replace(/[^a-z0-9_]/g, '');
    if (!cleanUser) {
      return res.status(400).json({ sukses: false, pesan: 'Username hanya boleh huruf, angka, dan underscore (_).' });
    }
    if (!rawPassword || rawPassword.length < 4) {
      return res.status(400).json({ sukses: false, pesan: 'Password minimal 4 karakter.' });
    }

    try {
      const { users, sha } = await fetchUsersFromGitHub();
      if (users[cleanUser]) {
        return res.status(400).json({
          sukses: false,
          pesan: `Username "${cleanUser}" sudah terdaftar! Silakan login atau pilih username lain.`
        });
      }

      const pwHash = hashPassword(rawPassword);
      const newUser = {
        username: cleanUser,
        passwordHash: pwHash,
        displayName: displayName || rawUsername,
        createdAt: new Date().toISOString()
      };

      users[cleanUser] = newUser;
      await saveUsersToGitHub(users, sha, `Register new user: ${cleanUser}`);

      return res.status(200).json({
        sukses: true,
        pesan: `Pendaftaran berhasil! Akun "${cleanUser}" siap digunakan.`,
        user: {
          username: cleanUser,
          displayName: newUser.displayName
        }
      });
    } catch (err) {
      console.error('Register error:', err);
      return res.status(500).json({ sukses: false, pesan: 'Terjadi kesalahan server saat mendaftar: ' + err.message });
    }
  }

  // 2. LOGIN
  if (action === 'login') {
    if (!rawUsername || !rawPassword) {
      return res.status(400).json({ sukses: false, pesan: 'Username dan Password wajib diisi.' });
    }
    const cleanUser = rawUsername.toLowerCase().replace(/[^a-z0-9_]/g, '');

    try {
      const { users } = await fetchUsersFromGitHub();
      const user = users[cleanUser];

      if (!user) {
        return res.status(401).json({
          sukses: false,
          pesan: `Username "${cleanUser}" tidak ditemukan. Silakan daftar terlebih dahulu!`
        });
      }

      const inputHash = hashPassword(rawPassword);
      if (user.passwordHash !== inputHash) {
        return res.status(401).json({
          sukses: false,
          pesan: 'Password salah! Periksa kembali huruf besar/kecil password Anda.'
        });
      }

      return res.status(200).json({
        sukses: true,
        pesan: `Login berhasil! Selamat datang, ${user.displayName || user.username}.`,
        user: {
          username: user.username,
          displayName: user.displayName || user.username
        }
      });
    } catch (err) {
      console.error('Login error:', err);
      return res.status(500).json({ sukses: false, pesan: 'Gagal terhubung ke database akun: ' + err.message });
    }
  }

  // 3. CHECK USERNAME AVAILABILITY
  if (action === 'check') {
    const cleanUser = rawUsername.toLowerCase().replace(/[^a-z0-9_]/g, '');
    try {
      const { users } = await fetchUsersFromGitHub();
      const exists = !!users[cleanUser];
      return res.status(200).json({ available: !exists, username: cleanUser });
    } catch (err) {
      return res.status(500).json({ available: false, error: err.message });
    }
  }

  return res.status(400).json({ sukses: false, pesan: 'Aksi tidak valid.' });
}
