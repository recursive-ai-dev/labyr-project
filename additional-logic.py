#!/usr/bin/env node
const fs = require('fs-extra');
const path = require('path');
const { generate } = require('random-words');
const nlp = require('compromise');

const CONFIG = {
  depth: parseInt(process.argv[2]) || 4,
  branching: parseInt(process.argv[3]) || 3,
  root: process.argv[4] || './semantic-fs',
  seed: process.argv[5] || Date.now()
};

// Deterministic random for reproducible structures
let seed = CONFIG.seed;
const random = () => {
  const x = Math.sin(seed++) * 10000;
  return x - Math.floor(x);
};

const ONTOLOGIES = [
  {
    domain: 'concepts',
    templates: [
      { type: 'entity', pattern: (w) => `${w}_system`, ext: '.concept' },
      { type: 'process', pattern: (w) => `${w}_flow`, ext: '.process' },
      { type: 'attribute', pattern: (w) => `${w}_property`, ext: '.attr' }
    ],
    generator: (word, depth) => {
      const doc = nlp(word);
      const isPlural = doc.nouns().isPlural().out('array').length > 0;
      return `Entity: ${word}\nState: ${isPlural ? 'aggregate' : 'singular'}\nDepth: ${depth}\nRelations: ${generate(2).join(', ')}\n`;
    }
  },
  {
    domain: 'temporal',
    templates: [
      { type: 'event', pattern: (w) => `${w}_event`, ext: '.chrono' },
      { type: 'sequence', pattern: (w) => `pre_${w}`, ext: '.seq' },
      { type: 'state', pattern: (w) => `${w}_state`, ext: '.temp' }
    ],
    generator: (word, depth) => {
      const tenses = ['past', 'present', 'future'];
      const tense = tenses[Math.floor(random() * 3)];
      return `Event: ${word}\nTense: ${tense}\nTimestamp: ${Date.now() - Math.floor(random() * 100000)}\nDuration: ${Math.floor(random() * 100)}s\n`;
    }
  },
  {
    domain: 'spatial',
    templates: [
      { type: 'location', pattern: (w) => `${w}_space`, ext: '.geo' },
      { type: 'container', pattern: (w) => `${w}_volume`, ext: '.vol' },
      { type: 'vector', pattern: (w) => `${w}_direction`, ext: '.vec' }
    ],
    generator: (word, depth) => {
      const coords = [random() * 100, random() * 100, random() * 100];
      return `Location: ${word}\nCoords: [${coords.map(c => c.toFixed(2)).join(', ')}]\nDimension: ${depth}D\nDensity: ${random().toFixed(3)}\n`;
    }
  }
];

class SemanticFS {
  constructor() {
    this.nodes = new Map();
    this.edges = [];
  }

  async generate() {
    console.log(`🌱 Growing semantic filesystem (seed: ${CONFIG.seed})...`);
    await fs.emptyDir(CONFIG.root);
    
    for (const ontology of ONTOLOGIES) {
      const domainPath = path.join(CONFIG.root, ontology.domain);
      await this.growBranch(domainPath, ontology, CONFIG.depth, null);
    }
    
    await this.weaveRelations();
    await this.writeManifest();
    console.log(`✅ Generated semantic structure at ${path.resolve(CONFIG.root)}`);
    console.log(`   Nodes: ${this.nodes.size}, Relations: ${this.edges.length}`);
  }

  async growBranch(currentPath, ontology, remainingDepth, parentWord) {
    await fs.ensureDir(currentPath);
    
    const word = generate(1)[0];
    const doc = nlp(word);
    const noun = doc.nouns().out('text') || word;
    const verb = doc.verbs().out('text');
    
    // Store node metadata
    this.nodes.set(currentPath, {
      word, noun, verb, depth: CONFIG.depth - remainingDepth,
      ontology: ontology.domain, parent: parentWord
    });

    if (remainingDepth <= 0) {
      // Leaf node - create semantic files
      await this.createArtifacts(currentPath, ontology, word);
      return;
    }

    // Generate semantic children
    const children = [];
    const templates = ontology.templates;
    
    for (let i = 0; i < CONFIG.branching; i++) {
      const template = templates[Math.floor(random() * templates.length)];
      const childWord = generate(1)[0];
      const childName = template.pattern(childWord);
      const childPath = path.join(currentPath, childName);
      
      children.push({ path: childPath, word: childWord, template });
      
      // Create edge to parent
      if (parentWord) {
        this.edges.push({ from: parentWord, to: childWord, type: template.type });
      }
    }

    // Recursively grow
    for (const child of children) {
      await this.growBranch(child.path, ontology, remainingDepth - 1, word);
    }

    // Add "see also" references at this level
    if (random() > 0.7) {
      await this.createSeeAlso(currentPath, word);
    }
  }

  async createArtifacts(dirPath, ontology, contextWord) {
    // Create 1-3 files with semantic content
    const count = 1 + Math.floor(random() * 3);
    for (let i = 0; i < count; i++) {
      const template = ontology.templates[Math.floor(random() * templates.length)];
      const artifactWord = generate(1)[0];
      const filename = `${artifactWord}_${contextWord}${template.ext}`;
      const content = ontology.generator(artifactWord, CONFIG.depth);
      await fs.writeFile(path.join(dirPath, filename), content);
    }
  }

  async createSeeAlso(dirPath, contextWord) {
    // Create symlink to semantically related directory
    const allPaths = Array.from(this.nodes.keys());
    if (allPaths.length < 2) return;
    
    // Find node with related word (shared root or similar length)
    const related = allPaths.find(p => {
      const node = this.nodes.get(p);
      return node && node.word !== contextWord && 
             (node.word.length === contextWord.length || 
              node.word[0] === contextWord[0]);
    });

    if (related) {
      const linkName = `_see_also_${this.nodes.get(related).word}`;
      const linkPath = path.join(dirPath, linkName);
      try {
        await fs.ensureSymlink(related, linkPath, 'dir');
        this.edges.push({ from: contextWord, to: this.nodes.get(related).word, type: 'semantic_link' });
      } catch(e) {
        // Ignore permission errors
      }
    }
  }

  async weaveRelations() {
    // Create a global index of semantic connections
    const indexPath = path.join(CONFIG.root, '_ontology_index.json');
    const index = {
      generated: new Date().toISOString(),
      seed: CONFIG.seed,
      domains: ONTOLOGIES.map(o => o.domain),
      graph: {
        nodes: Array.from(this.nodes.entries()).map(([path, data]) => ({ path, ...data })),
        edges: this.edges
      }
    };
    await fs.writeFile(indexPath, JSON.stringify(index, null, 2));
  }

  async writeManifest() {
    const manifest = `SEMANTIC FILESYSTEM MANIFEST
============================
Root: ${CONFIG.root}
Generation Seed: ${CONFIG.seed}
Max Depth: ${CONFIG.depth}
Branching Factor: ${CONFIG.branching}

ONTOLOGIES:
${ONTOLOGIES.map(o => `  - ${o.domain}: ${o.templates.map(t => t.type).join(', ')}`).join('\n')}

STRUCTURE:
Total Nodes: ${this.nodes.size}
Total Relations: ${this.edges.length}
Cross-References: ${this.edges.filter(e => e.type === 'semantic_link').length}

INSPECTION:
  tree ${CONFIG.root} | head -30
  find ${CONFIG.root} -name "*.concept" | wc -l
  cat ${CONFIG.root}/_ontology_index.json | jq '.graph.edges'
`;
    await fs.writeFile(path.join(CONFIG.root, 'README.semantic'), manifest);
  }
}

// CLI
if (require.main === module) {
  if (process.argv.includes('--help') || process.argv.includes('-h')) {
    console.log(`
Usage: node semantic-fs.js [depth] [branching] [root] [seed]

Generates a semantic filesystem with:
  - depth: Recursion depth (default: 4)
  - branching: Children per node (default: 3)  
  - root: Output directory (default: ./semantic-fs)
  - seed: Random seed for reproducibility (default: timestamp)

Examples:
  node semantic-fs.js
  node semantic-fs.js 5 2 ./my-semantic-tree 12345
`);
    process.exit(0);
  }

  new SemanticFS().generate().catch(console.error);
}

module.exports = SemanticFS;
