#!/usr/bin/env node
const fs = require('fs-extra');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = process.argv[2] || './game-fs';
const STATE_FILE = path.join(ROOT, '.player-state.json');
const HIDDEN_PREFIX = '.';

// Game configuration: locked dirs, keys, and rewards
const WORLD_GEN = {
  rooms: [
    { name: 'entrance', tags: ['visitor'], gives: ['torch'], needs: [] },
    { name: 'dark-cavern', tags: ['shadow'], gives: ['key-rusty'], needs: ['torch'] },
    { name: 'crystal-spire', tags: ['magic'], gives: ['orb-seeing'], needs: ['key-rusty'] },
    { name: 'void-archive', tags: ['forbidden'], gives: ['master-key'], needs: ['orb-seeing', 'shadow'] },
    { name: 'sanctum', tags: ['final'], gives: ['victory'], needs: ['master-key'] }
  ],
  decoys: 8, // fake folders to hide the real ones
  traps: 2   // folders that remove tags
};

class GameFS {
  async init() {
    console.log('🎮 Generating secure filesystem...');
    await fs.ensureDir(ROOT);
    
    // Create player state (invisible on surface)
    await this.saveState({ tags: ['visitor'], visited: [], inventory: [] });
    
    // Generate world
    for (const room of WORLD_GEN.rooms) {
      await this.createRoom(room);
    }
    
    // Add decoy folders (normal looking, no mechanics)
    for (let i = 0; i < WORLD_GEN.decoys; i++) {
      const fake = `documents-${Math.random().toString(36).slice(2, 6)}`;
      await fs.ensureDir(path.join(ROOT, fake));
      await fs.writeFile(path.join(ROOT, fake, 'readme.txt'), 'Nothing of interest here.');
    }
    
    // Add trap folders
    for (let i = 0; i < WORLD_GEN.traps; i++) {
      const trapDir = path.join(ROOT, 'restricted-zone-' + i);
      await fs.ensureDir(trapDir);
      await fs.writeFile(path.join(trapDir, '.access'), JSON.stringify({ needs: ['admin'], removes: ['torch', 'key-rusty'] }));
      await fs.writeFile(path.join(trapDir, 'WARNING.txt'), 'Security breach detected. Confiscating items.');
    }
    
    // Create navigation wrapper
    await this.createNavigator();
    console.log(`\n✅ World created at: ${path.resolve(ROOT)}`);
    console.log(`💡 Use: ./${ROOT}/enter <folder-name>`);
    console.log(`🔍 Hint: 'ls -la' won't show locked doors until you have the right tags`);
  }

  async createRoom(room) {
    const dir = path.join(ROOT, room.name);
    await fs.ensureDir(dir);
    
    // Hidden access control file
    await fs.writeFile(path.join(dir, '.access'), JSON.stringify({
      needs: room.needs,
      gives: room.gives,
      tags: room.tags
    }));
    
    // Visible lore file (hints at requirements)
    const hints = room.needs.length > 0 
      ? `Sealed. Requires: ${room.needs.join(' + ')}\n`
      : 'Open to all visitors.\n';
    await fs.writeFile(path.join(dir, 'LORE.txt'), hints + `\nRoom tags: ${room.tags.join(', ')}`);
    
    // Hidden reward contents
    for (const item of room.gives) {
      await fs.writeFile(path.join(dir, `.${item}.acquired`), 
        `You found: ${item}\nGranted at: ${new Date().toISOString()}`);
    }
    
    // Create subdirectories that reference other rooms (puzzle links)
    if (room.name === 'crystal-spire') {
      // Hidden symlink to void-archive only visible with orb-seeing
      await fs.ensureSymlink(
        path.join(ROOT, 'void-archive'), 
        path.join(dir, '.rift-portal')
      );
    }
  }

  async createNavigator() {
    const script = `#!/bin/bash
# Filesystem Game Navigator
ROOT="$(cd "$(dirname "$0")" && pwd)"
STATE="$ROOT/.player-state.json"
TARGET="$1"

if [ -z "$TARGET" ]; then
  echo "🎮 Available locations:"
  ls -1 "$ROOT" | grep -v "^\\\\." | grep -v "enter$" | while read dir; do
    if [ -d "$ROOT/$dir" ]; then
      ACCESS=$(cat "$ROOT/$dir/.access" 2>/dev/null || echo '{"needs":[]}')
      NEEDS=$(echo "$ACCESS" | grep -o '"needs":\\[[^]]*\\]' | sed 's/.*:\\[//;s/\\]//;s/"//g')
      if [ -z "$NEEDS" ] || [ "$NEEDS" = "" ]; then
        echo "  📂 $dir (open)"
      else
        echo "  🔒 $dir (requires: $NEEDS)"
      fi
    fi
  done
  echo ""
  echo "Inventory: $(cat "$STATE" | grep -o '"tags":\\[[^]]*\\]' | sed 's/.*:\\[//;s/\\]//;s/"//g')"
  exit 0
fi

if [ ! -d "$ROOT/$TARGET" ]; then
  # Check if it's a hidden path (symlink) they can now see
  if [ -L "$ROOT/$TARGET" ]; then
    LINK_TARGET=$(readlink "$ROOT/$TARGET")
    echo "🌟 You discovered a hidden path!"
  else
    echo "❌ Location does not exist"
    exit 1
  fi
fi

ACCESS_FILE="$ROOT/$TARGET/.access"
if [ ! -f "$ACCESS_FILE" ]; then
  cd "$ROOT/$TARGET"
  echo "📂 Entering $TARGET (neutral zone)"
  exec bash
fi

NEEDS=$(cat "$ACCESS_FILE" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>console.log(JSON.parse(d).needs.join(' ')))")
GIVES=$(cat "$ACCESS_FILE" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>console.log(JSON.parse(d).gives.join(' ')))")

HAS_ALL=true
for NEED in $NEEDS; do
  if ! grep -q "\\\"$NEED\\\"" "$STATE"; then
    HAS_ALL=false
    MISSING="$NEED"
    break
  fi
done

if [ "$HAS_ALL" = false ]; then
  echo "🔒 ACCESS DENIED"
  echo "Missing: $MISSING"
  echo "Current tags: $(cat "$STATE" | grep -o '"tags":\\[[^]]*\\]' | sed 's/.*:\\[//;s/\\]//')"
  exit 1
fi

# Grant rewards
for ITEM in $GIVES; do
  if ! grep -q "\\\"$ITEM\\\"" "$STATE"; then
    node -e "
      const fs=require('fs');
      const s=JSON.parse(fs.readFileSync('$STATE'));
      if(!s.tags.includes('$ITEM')){s.tags.push('$ITEM');s.inventory.push('$ITEM');}
      fs.writeFileSync('$STATE',JSON.stringify(s,null,2));
    "
    echo "✨ Acquired: $ITEM"
  fi
done

# Record visit
node -e "
  const fs=require('fs');
  const s=JSON.parse(fs.readFileSync('$STATE'));
  if(!s.visited.includes('$TARGET')) s.visited.push('$TARGET');
  fs.writeFileSync('$STATE',JSON.stringify(s,null,2));
"

echo "🎮 Entering $TARGET..."
cd "$ROOT/$TARGET"
exec bash
`;
    await fs.writeFile(path.join(ROOT, 'enter'), script);
    await fs.chmod(path.join(ROOT, 'enter'), 0o755);
  }

  async saveState(state) {
    await fs.writeFile(STATE_FILE, JSON.stringify(state, null, 2));
  }

  // Admin command to peek at structure
  async reveal() {
    console.log('\n🔮 GM View - Full Structure:');
    const dirs = await fs.readdir(ROOT);
    for (const dir of dirs) {
      const full = path.join(ROOT, dir);
      if ((await fs.stat(full)).isDirectory() && !dir.startsWith('.')) {
        const access = await fs.readJson(path.join(full, '.access')).catch(() => ({ needs: [], gives: [] }));
        console.log(`${dir}: needs [${access.needs.join(', ')}] → gives [${access.gives.join(', ')}]`);
      }
    }
  }
}

// CLI
const cmd = process.argv[2];
if (cmd === '--reveal' || cmd === '-r') {
  new GameFS().reveal();
} else if (cmd === '--help' || cmd === '-h') {
  console.log(`
Game Filesystem Generator
Usage:
  node game-fs.js [root-dir]     Create new game world
  node game-fs.js --reveal       Show full map (spoiler)
  node game-fs.js --help         This message

Gameplay:
  cd into the root directory and use ./enter <folder>
  or run ./enter to see available paths and inventory.
  Hidden folders exist but won't appear in 'ls' until unlocked.
`);
} else {
  new GameFS().init();
}
