# Implementation Guide: Diegetic Dark Fantasy Filesystem

## Overview

This guide provides step-by-step instructions for implementing the complete diegetic dark fantasy filesystem, starting with the enhanced labyrinth engine and progressing through the desktop environment integration.

## Prerequisites

### Required Software
- **Python 3.9+** with pip
- **Node.js 16+** (for frontend components)
- **Git** for version control
- **Virtual environment manager** (venv, conda, or poetry)

### Development Tools
- **Code editor** (VS Code recommended)
- **Terminal** with Python support
- **Image editor** (for creating assets)
- **Audio editor** (for sound effects)

## Project Structure

```
labyr-project/
├── src/
│   ├── labyr/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── measure_space.py      # Mathematical foundations
│   │   │   ├── graph.py             # Labyrinth graph generation
│   │   │   ├── entropy.py           # Entropy calculations
│   │   │   ├── combinatorics.py     # Path generation
│   │   │   └── character.py         # RPG character system
│   │   ├── rpg/
│   │   │   ├── progression.py       # Progression mechanics
│   │   │   ├── discovery.py         # Discovery system
│   │   │   ├── lore.py             # Narrative generation
│   │   │   └── difficulty.py        # Dynamic difficulty
│   │   ├── enhanced_graph.py        # Enhanced labyrinth with RPG
│   │   ├── api.py                   # Main API interface
│   │   └── cli.py                   # Command-line interface
│   ├── desktop/
│   │   ├── environment.py           # Desktop environment renderer
│   │   ├── themes.py               # Theme system
│   │   ├── cursor.py               # Diegetic cursor system
│   │   ├── notifications.py        # Contextual notifications
│   │   ├── audio.py                # Audio system
│   │   └── weather.py              # Weather and lighting
│   └── browser/
│       ├── main.py                 # Diegetic file browser
│       ├── ui.py                   # Fantasy UI components
│       └── interactions.py         # Interaction handlers
├── assets/
│   ├── themes/
│   │   ├── gothic_cityscape/
│   │   │   ├── background.jpg
│   │   │   ├── animations/
│   │   │   └── particles/
│   │   └── candlelit_library/
│   ├── cursors/
│   │   ├── spectral_hand.png
│   │   ├── magnifying_glass.png
│   │   └── glowing_orb.png
│   ├── fonts/
│   │   ├── ancient.ttf
│   │   └── ghostly.ttf
│   └── sounds/
│       ├── ambient/
│       ├── interactions/
│       └── discoveries/
├── tests/
│   ├── test_core/
│   ├── test_rpg/
│   ├── test_desktop/
│   └── test_integration/
├── docs/
│   ├── API.md
│   ├── USER_GUIDE.md
│   └── DEVELOPMENT.md
├── scripts/
│   ├── setup.py
│   ├── build.py
│   └── deploy.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Phase 1: Enhanced Labyrinth Engine (Week 1)

### Step 1: Set Up Project Structure

```bash
# Create project directory
mkdir labyr-project
cd labyr-project

# Initialize Python project
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip

# Create basic structure
mkdir -p src/labyr/core src/labyr/rpg src/labyr/tests assets/themes assets/cursors assets/fonts assets/sounds tests docs scripts
touch src/labyr/__init__.py src/labyr/core/__init__.py src/labyr/rpg/__init__.py
```

### Step 2: Install Dependencies

Create `requirements.txt`:

```txt
# Core dependencies
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0  # For visualization

# Development dependencies
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
ruff>=0.0.250
mypy>=0.991

# Optional: for enhanced functionality
pillow>=9.0.0  # Image processing
pygame>=2.1.0  # For desktop environment
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Implement Core Mathematical Components

Start by extracting and enhancing the existing mathematical components from `labyr-v0.6.py`:

```python
# src/labyr/core/measure_space.py
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, FrozenSet
import random
import math

class SemanticAlphabet(Enum):
    CITY = auto()
    DUNGEON = auto()
    HELL = auto()
    LABYRINTH = auto()
    FORTRESS = auto()
    PLAGUE = auto()
    CULT = auto()
    GRAVEYARD = auto()

@dataclass(frozen=True)
class SemanticElement:
    symbol: str
    theme: SemanticAlphabet
    category: str
    weight: float = 1.0
    
    def __post_init__(self):
        object.__setattr__(self, 'weight', max(0.0, min(1.0, self.weight)))
        object.__setattr__(self, 'entropy', -math.log2(self.weight) if self.weight > 0 else float('inf'))

class SemanticMeasureSpace:
    def __init__(self):
        self.Ω: Dict[SemanticAlphabet, Dict[str, List[SemanticElement]]] = {}
        self.transition_kernel: Dict[SemanticAlphabet, Dict[SemanticAlphabet, float]] = {}
        self._initialize_sample_space()
        self._construct_transition_kernel()
        self._validate_measure()
    
    def _initialize_sample_space(self):
        # Implement the semantic space from labyr-v0.6.py
        # ... (copy and adapt from existing implementation)
        pass
    
    def _construct_transition_kernel(self):
        # Implement Markov transition kernel
        # ... (copy and adapt from existing implementation)
        pass
    
    def sample_element(self, theme: SemanticAlphabet, category: str = None) -> SemanticElement:
        # Implement weighted sampling
        # ... (copy and adapt from existing implementation)
        pass
```

### Step 4: Implement RPG Character System

```python
# src/labyr/core/character.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class CharacterStats:
    """RPG character statistics affecting labyrinth interaction."""
    level: int = 1
    knowledge: int = 0      # Unlocks thematic areas
    courage: int = 0        # Required for dangerous areas
    perception: int = 0     # Affects discovery chance
    inventory: List[str] = field(default_factory=list)
    
    def can_access_theme(self, theme: 'SemanticAlphabet') -> bool:
        """Check if character can access theme based on stats."""
        theme_requirements = {
            'HELL': self.courage >= 10,
            'CULT': self.knowledge >= 15,
            'PLAGUE': self.courage >= 5,
            'LABYRINTH': self.perception >= 8,
        }
        return theme_requirements.get(theme.name, True)
    
    def gain_experience(self, amount: int):
        """Gain experience and level up if threshold reached."""
        self.knowledge += amount
        level_threshold = self.level * 100
        if self.knowledge >= level_threshold:
            self.level += 1
            # Distribute stat points
            self.courage += 2
            self.perception += 2
```

### Step 5: Create Enhanced Labyrinth Graph

```python
# src/labyr/enhanced_graph.py
from typing import Set, Dict, Tuple, Optional
from dataclasses import dataclass
from .core.graph import LabyrinthGraph
from .core.character import CharacterStats
from .rpg.progression import ProgressionSystem
from .rpg.discovery import DiscoverySystem
from .rpg.lore import LoreEngine
from .rpg.difficulty import DynamicDifficultySystem

@dataclass
class LabyrinthNode:
    id: str
    path: str
    depth: int
    theme: 'SemanticAlphabet'
    children: Set[str] = field(default_factory=set)
    entropy: float = 0.0
    lore: str = ""
    access_requirements: Dict = field(default_factory=dict)

class EnhancedLabyrinthGraph(LabyrinthGraph):
    """Enhanced graph with RPG mechanics integration."""
    
    def __init__(self, max_depth: int, branching_factor: int, chaos: float, 
                 measure_space: 'SemanticMeasureSpace', character: CharacterStats):
        super().__init__(max_depth, branching_factor, chaos, measure_space)
        self.character = character
        self.progression_system = ProgressionSystem(character)
        self.discovery_system = DiscoverySystem(measure_space)
        self.lore_engine = LoreEngine()
        self.difficulty_system = DynamicDifficultySystem(character)
        
    def generate_with_rpg_mechanics(self, target_vertices: int) -> Set[str]:
        """Generate labyrinth with RPG mechanics integrated."""
        # Adjust parameters based on character progression
        adjusted_params = self.difficulty_system.adjust_generation_parameters({
            'depth': self.max_depth,
            'breadth': self.branching_factor,
            'chaos': self.chaos
        })
        
        self.max_depth = adjusted_params['depth']
        self.branching_factor = adjusted_params['breadth']
        self.chaos = adjusted_params['chaos']
        
        # Generate base graph
        paths = super().generate(target_vertices)
        
        # Add RPG elements
        self._add_rpg_elements(paths)
        
        return paths
    
    def _add_rpg_elements(self, paths: Set[str]):
        """Add RPG elements to generated paths."""
        for path in paths:
            node = self.vertices[path]
            
            # Generate lore
            node.lore = self.lore_engine.generate_directory_lore(node, self.character)
            
            # Check for hidden nodes
            if random.random() < self.difficulty_system.adjusted_params.get('hidden_chance', 0.1):
                hidden = self.discovery_system.generate_hidden_node(node)
                if hidden:
                    self.vertices[hidden.path] = hidden
                    node.children.add(hidden.path)
            
            # Calculate access requirements
            node.access_requirements = self.progression_system.calculate_access_requirements(node)
    
    def attempt_access(self, path: str) -> Dict[str, any]:
        """Attempt to access a node with RPG mechanics."""
        if path not in self.vertices:
            return {'success': False, 'error': 'Path not found'}
            
        node = self.vertices[path]
        
        # Check progression requirements
        can_access, missing = self.progression_system.check_access(node)
        
        if not can_access:
            return {
                'success': False,
                'error': f'Access denied. Missing: {", ".join(missing)}',
                'lore': node.lore
            }
        
        # Grant access
        self.progression_system.grant_access(node)
        
        # Attempt discovery
        discovery_result = self.discovery_system.attempt_discovery(node, self.character)
        
        return {
            'success': True,
            'lore': node.lore,
            'discovery': discovery_result,
            'rewards': self._calculate_rewards(node)
        }
```

### Step 6: Create Main API

```python
# src/labyr/api.py
from typing import Dict, Any, List
from .core.measure_space import SemanticMeasureSpace
from .core.character import CharacterStats
from .enhanced_graph import EnhancedLabyrinthGraph

class LabyrinthAPI:
    """Main API for interacting with the enhanced labyrinth."""
    
    def __init__(self):
        self.character = CharacterStats()
        self.measure_space = SemanticMeasureSpace()
        self.graph = EnhancedLabyrinthGraph(5, 4, 0.3, self.measure_space, self.character)
        
    def generate_labyrinth(self, target_vertices: int = 100) -> Dict[str, Any]:
        """Generate a new labyrinth with RPG mechanics."""
        paths = self.graph.generate_with_rpg_mechanics(target_vertices)
        
        return {
            'paths': list(paths),
            'character_stats': self.character.__dict__,
            'generation_info': {
                'total_vertices': len(paths),
                'max_depth': self.graph.max_depth,
                'themes_used': list(set(self.graph.vertices[p].theme.name for p in paths))
            }
        }
    
    def explore_path(self, path: str) -> Dict[str, Any]:
        """Attempt to explore a specific path."""
        result = self.graph.attempt_access(path)
        
        return {
            'path': path,
            'character_stats': self.character.__dict__,
            'exploration_result': result
        }
    
    def get_character_status(self) -> Dict[str, Any]:
        """Get current character status and progression."""
        return {
            'stats': self.character.__dict__,
            'unlocked_areas': list(self.graph.progression_system.unlocked_areas),
            'inventory': self.character.inventory,
            'next_level_progress': {
                'current_xp': self.character.knowledge,
                'next_level_xp': self.character.level * 100,
                'progress_percent': (self.character.knowledge / (self.character.level * 100)) * 100
            }
        }
```

### Step 7: Create CLI Interface

```python
# src/labyr/cli.py
import argparse
import json
from .api import LabyrinthAPI

def main():
    parser = argparse.ArgumentParser(description="Diegetic Dark Fantasy Filesystem")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate labyrinth')
    gen_parser.add_argument('--count', '-c', type=int, default=100, help='Number of paths to generate')
    gen_parser.add_argument('--output', '-o', type=str, help='Output file for labyrinth data')
    
    # Explore command
    exp_parser = subparsers.add_parser('explore', help='Explore a path')
    exp_parser.add_argument('path', help='Path to explore')
    
    # Status command
    subparsers.add_parser('status', help='Show character status')
    
    args = parser.parse_args()
    
    api = LabyrinthAPI()
    
    if args.command == 'generate':
        result = api.generate_labyrinth(args.count)
        print(f"Generated {len(result['paths'])} paths")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Saved to {args.output}")
    
    elif args.command == 'explore':
        result = api.explore_path(args.path)
        print(f"Exploring: {args.path}")
        print(f"Success: {result['exploration_result']['success']}")
        if result['exploration_result']['success']:
            print(f"Lore: {result['exploration_result']['lore']}")
            if result['exploration_result']['discovery']['success']:
                print(f"Discovery: {result['exploration_result']['discovery']['reward']}")
    
    elif args.command == 'status':
        status = api.get_character_status()
        print(f"Level: {status['stats']['level']}")
        print(f"Knowledge: {status['stats']['knowledge']}")
        print(f"Courage: {status['stats']['courage']}")
        print(f"Perception: {status['stats']['perception']}")
        print(f"Inventory: {', '.join(status['inventory'])}")

if __name__ == '__main__':
    main()
```

### Step 8: Create Setup and Entry Points

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "labyr"
version = "0.1.0"
description = "Diegetic Dark Fantasy Filesystem"
authors = [{name = "Your Name", email = "your.email@example.com"}]
dependencies = [
    "numpy>=1.21.0",
    "scipy>=1.7.0",
]

[project.scripts]
labyr = "labyr.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
labyr = ["assets/**/*"]
```

### Step 9: Test the Enhanced Engine

Create basic tests:

```python
# tests/test_core/test_character.py
import unittest
from src.labyr.core.character import CharacterStats

class TestCharacterSystem(unittest.TestCase):
    def test_level_up(self):
        character = CharacterStats()
        character.gain_experience(100)
        self.assertEqual(character.level, 2)
        self.assertEqual(character.courage, 2)
        self.assertEqual(character.perception, 2)

    def test_theme_access(self):
        character = CharacterStats(level=5, courage=15)
        
        # Should be able to access most themes
        self.assertTrue(character.can_access_theme(SemanticAlphabet.CITY))
        self.assertTrue(character.can_access_theme(SemanticAlphabet.DUNGEON))
        
        # Should not be able to access HELL without enough courage
        self.assertFalse(character.can_access_theme(SemanticAlphabet.HELL))

if __name__ == '__main__':
    unittest.main()
```

Run tests:

```bash
python -m pytest tests/ -v
```

## Phase 2: Desktop Environment (Week 2)

### Step 1: Install Desktop Dependencies

Add to `requirements.txt`:

```txt
# Desktop environment dependencies
pygame>=2.1.0
Pillow>=9.0.0
```

### Step 2: Create Basic Desktop Environment

```python
# src/labyr/desktop/environment.py
import pygame
import random
import math
from typing import Dict, Tuple, Optional
from .themes import Theme
from .weather import WeatherSystem
from .audio import AudioSystem

class EnvironmentRenderer:
    """Manages the diegetic desktop background and environmental effects."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        pygame.display.set_caption("Diegetic Dark Fantasy Filesystem")
        
        self.current_theme = "gothic_cityscape"
        self.weather_system = WeatherSystem()
        self.audio_system = AudioSystem()
        
        # Initialize theme
        from .themes import GothicCityscapeTheme
        self.apply_theme(GothicCityscapeTheme())
        
    def apply_theme(self, theme: Theme):
        """Apply a theme's visual and audio properties."""
        self.current_theme_config = theme
        self.audio_system.set_theme(theme)
        
    def render_frame(self):
        """Render a single frame of the environment."""
        # Clear screen
        self.screen.fill(self.current_theme_config.color_scheme['primary'])
        
        # Update and render weather effects
        weather_effects = self.weather_system.get_current_effects()
        self.render_weather_effects(weather_effects)
        
        # Render background elements
        self.render_background_elements()
        
        # Update display
        pygame.display.flip()
        
    def render_weather_effects(self, effects: Dict):
        """Render weather-specific effects."""
        if effects['type'] == 'rain':
            self.render_rain_effects(effects['intensity'])
        elif effects['type'] == 'fog':
            self.render_fog_effects(effects['intensity'])
            
    def render_rain_effects(self, intensity: float):
        """Render rain particle effects."""
        for _ in range(int(50 * intensity)):
            x = random.randint(0, 1920)
            y = random.randint(0, 1080)
            length = random.randint(10, 20)
            pygame.draw.line(self.screen, (200, 200, 255), (x, y), (x, y + length), 1)
            
    def run(self):
        """Main rendering loop."""
        clock = pygame.time.Clock()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update systems
            self.weather_system.update()
            
            # Render frame
            self.render_frame()
            
            # Cap at 60 FPS
            clock.tick(60)
            
        pygame.quit()
```

### Step 3: Create Theme System

```python
# src/labyr/desktop/themes.py
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Theme:
    """Base theme configuration."""
    name: str
    background_config: Dict
    color_scheme: Dict
    ambient_sounds: List[str]
    particle_config: Dict
    cursor_styles: Dict
    notification_styles: Dict

class GothicCityscapeTheme(Theme):
    """Gothic cityscape viewed from a tower window."""
    
    def __init__(self):
        super().__init__(
            name="gothic_cityscape",
            background_config={
                'type': 'animated',
                'base_image': 'assets/themes/gothic_cityscape/base.jpg',
                'animations': [
                    {'layer': 'sky', 'animation': 'cloud_drift', 'speed': 0.1},
                    {'layer': 'city', 'animation': 'flicker_lights', 'speed': 0.5},
                    {'layer': 'foreground', 'animation': 'rain_particles', 'speed': 2.0}
                ]
            },
            color_scheme={
                'primary': (42, 26, 61),    # Deep purple
                'secondary': (139, 0, 0),   # Dark red
                'accent': (255, 215, 0),    # Gold
                'text': (255, 255, 255),    # White
                'shadow': (0, 0, 0)         # Black
            },
            ambient_sounds=[
                'distant_thunder.wav',
                'city_ambience.wav',
                'wind_whistling.wav',
                'church_bells.wav'
            ],
            particle_config={
                'rain': {'density': 0.8, 'speed': 2.0, 'size': 2},
                'dust': {'density': 0.3, 'speed': 0.1, 'size': 1},
                'embers': {'density': 0.1, 'speed': 0.5, 'size': 3}
            },
            cursor_styles={
                'default': 'spectral_hand',
                'hover': 'glowing_orb',
                'click': 'shadow_tendril'
            },
            notification_styles={
                'scroll': 'ancient_parchment',
                'whisper': 'ghostly_text',
                'rune': 'magical_glyph'
            }
        )
```

### Step 4: Create Diegetic Cursor System

```python
# src/labyr/desktop/cursor.py
import pygame
from typing import Optional, Dict, Tuple

class DiegeticCursor:
    """Manages the fantasy-themed cursor system."""
    
    def __init__(self, renderer):
        self.renderer = renderer
        self.current_style = "spectral_hand"
        self.position = (0, 0)
        self.hover_state = None
        self.animation_frame = 0
        
    def update(self, mouse_x: int, mouse_y: int, hover_target: Optional[str]):
        """Update cursor position and state."""
        self.position = (mouse_x, mouse_y)
        self.hover_state = hover_target
        
        # Update animation frame
        self.animation_frame = (self.animation_frame + 1) % 60
        
        # Determine appropriate cursor style based on context
        self.current_style = self.get_contextual_style(hover_target)
        
    def get_contextual_style(self, hover_target: Optional[str]) -> str:
        """Determine cursor style based on what's being hovered."""
        if hover_target is None:
            return self.renderer.current_theme_config.cursor_styles['default']
            
        # Context-specific cursor styles
        if 'scroll' in hover_target or 'document' in hover_target:
            return 'magnifying_glass'
        elif 'key' in hover_target or 'lock' in hover_target:
            return 'glowing_orb'
        elif 'danger' in hover_target or 'cursed' in hover_target:
            return 'shadow_tendril'
        elif 'magic' in hover_target or 'portal' in hover_target:
            return 'arcane_hand'
        else:
            return self.renderer.current_theme_config.cursor_styles['hover']
            
    def render(self, surface):
        """Render the cursor at current position."""
        # Get cursor configuration
        cursor_config = self.get_cursor_config()
        
        # Apply hover effects
        if self.hover_state:
            cursor_config = self.apply_hover_effects(cursor_config)
            
        # Render cursor
        self.render_cursor_animation(surface, cursor_config)
        
    def get_cursor_config(self) -> Dict:
        """Get configuration for current cursor style."""
        styles = {
            'spectral_hand': {
                'color': (255, 255, 255),
                'size': 20,
                'glow_radius': 10,
                'animation_frames': 8
            },
            'magnifying_glass': {
                'color': (255, 215, 0),
                'size': 25,
                'magnification': 1.5,
                'glow_radius': 5
            },
            'glowing_orb': {
                'color': (0, 255, 255),
                'size': 15,
                'pulse_speed': 0.1,
                'color_shift': True
            }
        }
        
        return styles.get(self.current_style, styles['spectral_hand'])
        
    def render_cursor_animation(self, surface, config: Dict):
        """Render animated cursor."""
        x, y = self.position
        size = config['size']
        
        # Create cursor surface
        cursor_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        
        # Draw cursor shape based on style
        if self.current_style == 'spectral_hand':
            pygame.draw.circle(cursor_surface, config['color'], (size, size), size)
            # Add spectral effect
            pygame.draw.circle(cursor_surface, (255, 255, 255, 100), (size, size), size + 5, 2)
            
        elif self.current_style == 'magnifying_glass':
            pygame.draw.circle(cursor_surface, config['color'], (size, size), size)
            pygame.draw.circle(cursor_surface, (255, 255, 255), (size, size), size - 3, 2)
            
        elif self.current_style == 'glowing_orb':
            # Pulse effect
            pulse = math.sin(pygame.time.get_ticks() * 0.01) * 5
            pygame.draw.circle(cursor_surface, config['color'], (size, size), size + pulse)
            
        # Blit to main surface
        surface.blit(cursor_surface, (x - size, y - size))
```

### Step 5: Integrate with Labyrinth API

```python
# src/labyr/desktop/main.py
import pygame
from .environment import EnvironmentRenderer
from .cursor import DiegeticCursor
from ..api import LabyrinthAPI

class DesktopEnvironment:
    """Main interface for diegetic desktop environment."""
    
    def __init__(self):
        self.labyrinth_api = LabyrinthAPI()
        self.renderer = EnvironmentRenderer()
        self.cursor = DiegeticCursor(self.renderer)
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        pygame.display.set_caption("Diegetic Dark Fantasy Filesystem")
        
        # Hide default cursor
        pygame.mouse.set_visible(False)
        
    def run(self):
        """Main application loop."""
        clock = pygame.time.Clock()
        
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.cursor.update(event.pos[0], event.pos[1], None)
            
            # Update environment
            self.renderer.weather_system.update()
            
            # Render frame
            self.renderer.render_frame()
            
            # Render cursor
            self.cursor.render(self.screen)
            
            # Update display
            pygame.display.flip()
            
            # Cap at 60 FPS
            clock.tick(60)
            
        pygame.quit()
        
    def handle_mouse_click(self, event):
        """Handle mouse clicks for file operations."""
        # Convert screen coordinates to file path
        # This would integrate with the actual file system
        pass

if __name__ == '__main__':
    env = DesktopEnvironment()
    env.run()
```

## Phase 3: Integration and Polish (Week 3)

### Step 1: Create File System Integration

```python
# src/labyr/filesystem.py
import os
import json
from pathlib import Path
from typing import Dict, Any, List
from .api import LabyrinthAPI

class FileSystemManager:
    """Manages the actual file system integration."""
    
    def __init__(self, base_path: str = "./labyrinth"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.labyrinth_api = LabyrinthAPI()
        
    def generate_filesystem(self, target_vertices: int = 100):
        """Generate the actual filesystem structure."""
        result = self.labyrinth_api.generate_labyrinth(target_vertices)
        
        # Create directories
        for path in result['paths']:
            full_path = self.base_path / path
            full_path.mkdir(parents=True, exist_ok=True)
            
            # Create lore file
            lore_file = full_path / "LORE.txt"
            node = self.labyrinth_api.graph.vertices[path]
            lore_file.write_text(node.lore)
            
            # Create some thematic files
            self.create_thematic_files(full_path, node)
            
        # Save labyrinth metadata
        metadata_file = self.base_path / ".labyrinth_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(result, f, indent=2)
            
    def create_thematic_files(self, path: Path, node):
        """Create thematic files in a directory."""
        # Create some example files based on theme
        theme_files = {
            'CITY': ['city_records.txt', 'map_fragment.png', 'merchant_ledger.txt'],
            'DUNGEON': ['prisoner_diary.txt', 'torture_log.txt', 'escape_plan.txt'],
            'HELL': ['summoning_runes.txt', 'demon_contract.txt', 'soul_ledger.txt'],
        }
        
        files = theme_files.get(node.theme.name, ['mysterious_document.txt'])
        
        for filename in files:
            file_path = path / filename
            content = self.labyrinth_api.graph.lore_engine.generate_file_content(filename, node)
            file_path.write_text(content)
```

### Step 2: Create Complete Application

```python
# src/labyr/__main__.py
import argparse
import sys
from .filesystem import FileSystemManager
from .desktop.main import DesktopEnvironment

def main():
    parser = argparse.ArgumentParser(description="Diegetic Dark Fantasy Filesystem")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate filesystem')
    gen_parser.add_argument('--count', '-c', type=int, default=100, help='Number of paths')
    gen_parser.add_argument('--path', '-p', type=str, default='./labyrinth', help='Base path')
    
    # Desktop command
    subparsers.add_parser('desktop', help='Launch desktop environment')
    
    args = parser.parse_args()
    
    if args.command == 'generate':
        manager = FileSystemManager(args.path)
        manager.generate_filesystem(args.count)
        print(f"Generated filesystem at {args.path}")
        
    elif args.command == 'desktop':
        env = DesktopEnvironment()
        env.run()
        
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

### Step 3: Create Asset Pipeline

Create a simple asset management system:

```python
# scripts/setup_assets.py
import os
import shutil
from pathlib import Path

def setup_assets():
    """Set up the asset directory structure."""
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    # Create theme directories
    themes = ["gothic_cityscape", "candlelit_library"]
    for theme in themes:
        (assets_dir / "themes" / theme).mkdir(parents=True, exist_ok=True)
    
    # Create other asset directories
    directories = [
        "cursors",
        "fonts", 
        "sounds/ambient",
        "sounds/interactions",
        "sounds/discoveries"
    ]
    
    for directory in directories:
        (assets_dir / directory).mkdir(parents=True, exist_ok=True)
    
    print("Asset directories created successfully!")

if __name__ == '__main__':
    setup_assets()
```

### Step 4: Create Build and Deployment Scripts

```python
# scripts/build.py
import os
import shutil
from pathlib import Path

def build():
    """Build the application for distribution."""
    print("Building application...")
    
    # Create build directory
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    
    # Copy source code
    shutil.copytree("src", build_dir / "src", dirs_exist_ok=True)
    
    # Copy assets
    shutil.copytree("assets", build_dir / "assets", dirs_exist_ok=True)
    
    # Create executable script
    with open(build_dir / "labyr.py", "w") as f:
        f.write("""#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from labyr.__main__ import main
if __name__ == '__main__':
    main()
""")
    
    print("Build complete!")

if __name__ == '__main__':
    build()
```

## Testing and Validation

### Unit Tests

```python
# tests/test_integration.py
import unittest
import tempfile
import shutil
from pathlib import Path
from src.labyr.filesystem import FileSystemManager
from src.labyr.api import LabyrinthAPI

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        
    def test_filesystem_generation(self):
        """Test that filesystem generation creates proper structure."""
        manager = FileSystemManager(self.temp_dir)
        manager.generate_filesystem(10)
        
        # Check that directories were created
        labyrinth_dirs = list(Path(self.temp_dir).glob("**/"))
        self.assertGreater(len(labyrinth_dirs), 5)
        
        # Check that lore files exist
        lore_files = list(Path(self.temp_dir).glob("**/LORE.txt"))
        self.assertGreater(len(lore_files), 0)
        
    def test_api_integration(self):
        """Test that API works correctly."""
        api = LabyrinthAPI()
        
        # Generate labyrinth
        result = api.generate_labyrinth(50)
        self.assertEqual(len(result['paths']), 50)
        
        # Check character progression
        initial_level = api.character.level
        api.character.gain_experience(100)
        self.assertEqual(api.character.level, initial_level + 1)

if __name__ == '__main__':
    unittest.main()
```

### Performance Testing

```python
# scripts/performance_test.py
import time
import psutil
from src.labyr.api import LabyrinthAPI

def performance_test():
    """Test performance of labyrinth generation."""
    print("Starting performance test...")
    
    # Monitor initial resources
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Test generation times
    sizes = [100, 500, 1000, 2000]
    
    for size in sizes:
        api = LabyrinthAPI()
        
        start_time = time.time()
        result = api.generate_labyrinth(size)
        end_time = time.time()
        
        generation_time = end_time - start_time
        final_memory = process.memory_info().rss / 1024 / 1024
        
        print(f"Size: {size:4d} | Time: {generation_time:.2f}s | Memory: {final_memory:.1f}MB")

if __name__ == '__main__':
    performance_test()
```

## Deployment

### Creating Distribution Package

```bash
# Build the package
python -m build

# Install locally for testing
pip install dist/labyr-0.1.0-py3-none-any.whl

# Run the application
labyr generate --count 200 --path ./my_labyrinth
labyr desktop
```

### Cross-Platform Considerations

For cross-platform deployment, consider using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/labyr/__main__.py
```

## Development Workflow

### Daily Development

1. **Start development environment:**
   ```bash
   source venv/bin/activate
   cd labyr-project
   ```

2. **Run tests:**
   ```bash
   python -m pytest tests/ -v
   ```

3. **Test generation:**
   ```bash
   python -m labyr generate --count 50
   ```

4. **Test desktop environment:**
   ```bash
   python -m labyr desktop
   ```

### Code Quality

1. **Format code:**
   ```bash
   black src/ tests/
   ```

2. **Check linting:**
   ```bash
   ruff check src/ tests/
   ```

3. **Type checking:**
   ```bash
   mypy src/
   ```

This implementation guide provides a comprehensive roadmap for building the complete diegetic dark fantasy filesystem, starting with the mathematical foundations and progressing through the immersive desktop environment integration.