# Technical Specification: Enhanced Labyrinth Engine with RPG Mechanics

## Overview

This document provides the technical specifications for enhancing the existing `labyr-v0.6.py` mathematical labyrinth generator with RPG mechanics while preserving its rigorous mathematical foundations.

## Current State Analysis

### Existing Mathematical Components (from `labyr-v0.6.py`)

1. **SemanticMeasureSpace**: Probability space with Markov transition kernels
2. **LabyrinthGraph**: DAG generation with topological constraints
3. **CombinatorialGenerator**: Path generation with collision detection
4. **Entropy Calculations**: Shannon entropy and Kolmogorov complexity estimation

### Required RPG Enhancements

1. **Character System**: User progression affecting labyrinth access
2. **Progression Mechanics**: Unlockable areas and abilities
3. **Discovery System**: Hidden nodes and exploration rewards
4. **Lore Engine**: Narrative content generation
5. **Dynamic Difficulty**: Scaling complexity based on user progression

## Enhanced Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ENHANCED LABYRINTH ENGINE                │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              MATHEMATICAL CORE (PRESERVED)              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ SemanticMeasure │  │ LabyrinthGraph  │              │ │
│  │  │ Space           │  │                 │              │ │
│  │  └─────────────────┘  └─────────────────┘              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Combinatorial   │  │ Entropy         │              │ │
│  │  │ Generator       │  │ Calculations    │              │ │
│  │  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 RPG MECHANICS LAYER                     │ │
│  │  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Character       │  │ Progression     │              │ │
│  │  │ System          │  │ System          │              │ │
│  │  └─────────────────┘  └─────────────────┘              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Discovery       │  │ Lore Engine     │              │ │
│  │  │ System          │  │                 │              │ │
│  │  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              INTEGRATION LAYER                          │ │
│  │  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Dynamic         │  │ Theme           │              │ │
│  │  │ Difficulty      │  │ Consistency     │              │ │
│  │  │ Scaling         │  │ Enforcement     │              │ │
│  │  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Component Specifications

### 1. Character System (`character.py`)

```python
@dataclass
class CharacterStats:
    """RPG character statistics affecting labyrinth interaction."""
    level: int = 1
    knowledge: int = 0      # Unlocks thematic areas
    courage: int = 0        # Required for dangerous areas
    perception: int = 0     # Affects discovery chance
    inventory: List[str] = field(default_factory=list)
    
    def can_access_theme(self, theme: SemanticAlphabet) -> bool:
        """Check if character can access theme based on stats."""
        theme_requirements = {
            SemanticAlphabet.HELL: self.courage >= 10,
            SemanticAlphabet.CULT: self.knowledge >= 15,
            SemanticAlphabet.PLAGUE: self.courage >= 5,
            SemanticAlphabet.LABYRINTH: self.perception >= 8,
        }
        return theme_requirements.get(theme, True)
    
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

### 2. Progression System (`progression.py`)

```python
class ProgressionSystem:
    """Manages progressive unlocking of labyrinth areas."""
    
    def __init__(self, character: CharacterStats):
        self.character = character
        self.unlocked_areas: Set[str] = set()
        self.completed_quests: List[str] = []
        
    def calculate_access_requirements(self, node: LabyrinthNode) -> Dict[str, Any]:
        """Calculate requirements for accessing a labyrinth node."""
        requirements = {
            'min_level': max(1, node.depth // 2),
            'required_stats': {},
            'keys_needed': [],
            'rituals_required': []
        }
        
        # Theme-specific requirements
        if node.theme == SemanticAlphabet.HELL:
            requirements['required_stats']['courage'] = 10 + node.depth
        elif node.theme == SemanticAlphabet.CULT:
            requirements['required_stats']['knowledge'] = 15 + node.depth
        elif node.theme == SemanticAlphabet.LABYRINTH:
            requirements['required_stats']['perception'] = 8 + node.depth
            
        # Special requirements for deep nodes
        if node.depth > 10:
            requirements['keys_needed'].append(f'key_depth_{node.depth}')
            
        return requirements
    
    def check_access(self, node: LabyrinthNode) -> Tuple[bool, List[str]]:
        """Check if character can access node and return missing requirements."""
        reqs = self.calculate_access_requirements(node)
        missing = []
        
        if self.character.level < reqs['min_level']:
            missing.append(f"Level {reqs['min_level']}")
            
        for stat, value in reqs['required_stats'].items():
            if getattr(self.character, stat) < value:
                missing.append(f"{stat.title()} {value}")
                
        for key in reqs['keys_needed']:
            if key not in self.character.inventory:
                missing.append(f"Key: {key}")
                
        return len(missing) == 0, missing
    
    def grant_access(self, node: LabyrinthNode):
        """Grant access to node and update progression."""
        self.unlocked_areas.add(node.path)
        
        # Grant rewards
        if node.depth > 5 and 'rare_artifact' not in self.character.inventory:
            self.character.inventory.append('rare_artifact')
            self.character.knowledge += 50
            
        # Unlock new themes based on exploration
        if node.theme == SemanticAlphabet.HELL and self.character.courage < 20:
            self.character.courage = 20
```

### 3. Discovery System (`discovery.py`)

```python
class DiscoverySystem:
    """Manages hidden nodes and exploration mechanics."""
    
    def __init__(self, measure_space: SemanticMeasureSpace):
        self.measure_space = measure_space
        self.discovered_nodes: Set[str] = set()
        self.hidden_nodes: Dict[str, Dict] = {}
        self.fog_of_war: Dict[str, bool] = {}
        
    def generate_hidden_node(self, parent_node: LabyrinthNode) -> Optional[LabyrinthNode]:
        """Generate a hidden node with special properties."""
        if random.random() > 0.1:  # 10% chance
            return None
            
        # Create hidden theme
        hidden_theme = random.choice(list(SemanticAlphabet))
        
        # Generate hidden name with discovery mechanics
        hidden_name = f"hidden_{random.choice(['chamber', 'vault', 'sanctum', 'archive'])}"
        hidden_path = f"{parent_node.path}/{hidden_name}"
        
        hidden_node = LabyrinthNode(
            id=hash(hidden_path),
            path=hidden_path,
            depth=parent_node.depth + 1,
            theme=hidden_theme,
            entropy=2.0  # High entropy for mystery
        )
        
        # Store hidden node properties
        self.hidden_nodes[hidden_path] = {
            'requires': random.choice(['ritual', 'key', 'perception_check']),
            'reward': random.choice(['lore_fragment', 'ancient_key', 'forbidden_knowledge']),
            'danger_level': random.randint(1, 5)
        }
        
        return hidden_node
    
    def calculate_discovery_chance(self, node: LabyrinthNode, character: CharacterStats) -> float:
        """Calculate chance of discovering hidden content."""
        base_chance = 0.3
        perception_bonus = character.perception * 0.02
        exploration_penalty = len(self.discovered_nodes) * 0.001
        
        # Theme-specific modifiers
        theme_modifiers = {
            SemanticAlphabet.LABYRINTH: 0.2,
            SemanticAlphabet.CULT: 0.1,
            SemanticAlphabet.GRAVEYARD: -0.1
        }
        
        theme_bonus = theme_modifiers.get(node.theme, 0)
        
        chance = base_chance + perception_bonus + theme_bonus - exploration_penalty
        return max(0.0, min(1.0, chance))
    
    def attempt_discovery(self, node: LabyrinthNode, character: CharacterStats) -> Dict[str, Any]:
        """Attempt to discover hidden content in node."""
        if random.random() < self.calculate_discovery_chance(node, character):
            # Success! Generate discovery content
            discovery_type = random.choice(['hidden_chamber', 'secret_passage', 'forgotten_tome'])
            
            if discovery_type == 'hidden_chamber':
                reward = f"Chamber of {node.theme.name} - Unlocks new abilities"
                character.perception += 5
            elif discovery_type == 'secret_passage':
                reward = "Secret passage discovered - New areas accessible"
                # Add new connections to graph
            else:  # forgotten_tome
                reward = "Forgotten tome found - Gains knowledge"
                character.knowledge += 20
                
            self.discovered_nodes.add(node.path)
            return {'success': True, 'type': discovery_type, 'reward': reward}
        else:
            return {'success': False, 'message': 'Nothing found... yet.'}
```

### 4. Lore Engine (`lore.py`)

```python
class LoreEngine:
    """Generates narrative content for labyrinth elements."""
    
    def __init__(self):
        self.story_arcs = self._load_story_arcs()
        self.narrative_templates = self._load_templates()
        
    def _load_story_arcs(self) -> Dict[str, Dict]:
        """Load predefined story arcs."""
        return {
            'forbidden_library': {
                'title': 'The Forbidden Library',
                'chapters': [
                    'The Guardian\'s Warning',
                    'The First Forbidden Tome',
                    'The Librarian\'s Secret',
                    'The Final Chapter'
                ],
                'themes': [SemanticAlphabet.CITY, SemanticAlphabet.CULT, SemanticAlphabet.GRAVEYARD]
            },
            'haunted_archive': {
                'title': 'The Haunted Archive',
                'chapters': [
                    'Whispers in the Stacks',
                    'The Cursed Catalogue',
                    'Echoes of the Past',
                    'Breaking the Curse'
                ],
                'themes': [SemanticAlphabet.CITY, SemanticAlphabet.PLAGUE, SemanticAlphabet.GRAVEYARD]
            }
        }
    
    def _load_templates(self) -> Dict[str, List[str]]:
        """Load narrative templates for different elements."""
        return {
            'directory': [
                "This {theme} holds the secrets of {mystery}.",
                "Within these {theme} walls lies knowledge best forgotten.",
                "The {theme} hums with ancient power, waiting to be understood."
            ],
            'file': [
                "A {type} containing fragments of {content}.",
                "This {type} whispers secrets of the {theme}.",
                "Within this {type} lies the key to {mystery}."
            ],
            'hidden': [
                "A hidden {type} pulses with forbidden energy.",
                "This {type} was meant to remain undiscovered.",
                "The {type} contains truths that could drive one mad."
            ]
        }
    
    def generate_directory_lore(self, node: LabyrinthNode, character: CharacterStats) -> str:
        """Generate lore for a directory node."""
        template = random.choice(self.narrative_templates['directory'])
        
        lore_data = {
            'theme': node.theme.name.lower(),
            'mystery': random.choice(['ancient prophecies', 'forbidden rituals', 'lost civilizations']),
            'depth': node.depth,
            'character_level': character.level
        }
        
        # Add progression-based lore
        if character.level > 10:
            lore_data['mystery'] = f"secrets only the worthy can comprehend"
        elif node.depth > 8:
            lore_data['mystery'] = f"dangerous knowledge that tests the brave"
            
        return template.format(**lore_data)
    
    def generate_file_content(self, filename: str, node: LabyrinthNode) -> str:
        """Generate thematic content for a file."""
        file_type = filename.split('.')[-1] if '.' in filename else 'text'
        
        if 'hidden' in filename or node.depth > 10:
            template = random.choice(self.narrative_templates['hidden'])
        else:
            template = random.choice(self.narrative_templates['file'])
            
        content_data = {
            'type': file_type,
            'theme': node.theme.name.lower(),
            'content': random.choice(['ancient runes', 'cryptic symbols', 'forbidden incantations']),
            'mystery': random.choice(['eternal truths', 'cosmic secrets', 'divine mysteries'])
        }
        
        return template.format(**content_data)
    
    def generate_quest_description(self, node: LabyrinthNode) -> str:
        """Generate a quest description for exploring a node."""
        quests = {
            SemanticAlphabet.HELL: "Seek the infernal knowledge hidden in the flames.",
            SemanticAlphabet.CULT: "Uncover the cult's forbidden rituals.",
            SemanticAlphabet.LABYRINTH: "Navigate the maze and find the center.",
            SemanticAlphabet.PLAGUE: "Find the source of the corruption.",
            SemanticAlphabet.GRAVEYARD: "Discover what lies beneath the earth.",
            SemanticAlphabet.FORTRESS: "Breaching the walls of power.",
            SemanticAlphabet.DUNGEON: "Survive the depths and return with knowledge.",
            SemanticAlphabet.CITY: "Explore the secrets of the urban sprawl."
        }
        
        base_quest = quests.get(node.theme, "Explore this area and uncover its secrets.")
        
        if node.depth > 5:
            base_quest += " This area is particularly dangerous."
        if node.depth > 10:
            base_quest += " Legends speak of unimaginable power here."
            
        return base_quest
```

### 5. Dynamic Difficulty System (`difficulty.py`)

```python
class DynamicDifficultySystem:
    """Adjusts labyrinth complexity based on character progression."""
    
    def __init__(self, character: CharacterStats):
        self.character = character
        self.base_complexity = 1.0
        self.adaptation_rate = 0.1
        
    def calculate_complexity_multiplier(self) -> float:
        """Calculate complexity multiplier based on character stats."""
        # Base complexity increases with level
        level_factor = 1.0 + (self.character.level * 0.1)
        
        # Knowledge affects semantic complexity
        knowledge_factor = 1.0 + (self.character.knowledge * 0.001)
        
        # Courage affects dangerous theme frequency
        courage_factor = 1.0 + (self.character.courage * 0.005)
        
        # Perception affects discovery density
        perception_factor = 1.0 + (self.character.perception * 0.002)
        
        return level_factor * knowledge_factor * courage_factor * perception_factor
    
    def adjust_generation_parameters(self, base_params: Dict) -> Dict:
        """Adjust labyrinth generation parameters based on difficulty."""
        multiplier = self.calculate_complexity_multiplier()
        
        adjusted = base_params.copy()
        
        # Increase depth for higher levels
        adjusted['depth'] = min(20, base_params['depth'] + int(self.character.level * 0.5))
        
        # Increase branching for complex players
        adjusted['breadth'] = min(15, base_params['breadth'] + int(self.character.knowledge * 0.1))
        
        # Adjust chaos factor based on courage
        base_chaos = base_params.get('chaos', 0.3)
        courage_chaos = base_chaos + (self.character.courage * 0.01)
        adjusted['chaos'] = min(0.8, max(0.1, courage_chaos))
        
        # Increase hidden node density for perceptive players
        base_hidden_chance = base_params.get('hidden_chance', 0.1)
        perception_hidden = base_hidden_chance + (self.character.perception * 0.005)
        adjusted['hidden_chance'] = min(0.3, perception_hidden)
        
        return adjusted
    
    def calculate_reward_scaling(self) -> float:
        """Calculate reward scaling based on difficulty."""
        # Higher difficulty = better rewards
        difficulty_score = (
            self.character.level * 10 +
            self.character.knowledge * 0.5 +
            self.character.courage * 2 +
            self.character.perception
        )
        
        # Exponential scaling for high-level play
        return 1.0 + (difficulty_score * 0.05)
```

## Integration Layer

### Enhanced LabyrinthGraph (`enhanced_graph.py`)

```python
class EnhancedLabyrinthGraph(LabyrinthGraph):
    """Enhanced graph with RPG mechanics integration."""
    
    def __init__(self, max_depth: int, branching_factor: int, chaos: float, 
                 measure_space: SemanticMeasureSpace, character: CharacterStats):
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
    
    def attempt_access(self, path: str) -> Dict[str, Any]:
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
    
    def _calculate_rewards(self, node: LabyrinthNode) -> List[str]:
        """Calculate rewards for accessing a node."""
        rewards = []
        
        # Base experience reward
        exp_reward = node.depth * 10
        self.character.knowledge += exp_reward
        rewards.append(f'Gained {exp_reward} knowledge')
        
        # Special rewards for deep nodes
        if node.depth > 10:
            rewards.append('Unlocked new abilities')
            
        # Theme-specific rewards
        if node.theme == SemanticAlphabet.HELL:
            rewards.append('Gained courage from facing fears')
        elif node.theme == SemanticAlphabet.CULT:
            rewards.append('Learned forbidden secrets')
            
        return rewards
```

## API Specification

### Core API Endpoints

```python
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

## Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Generate lore and discovery content only when accessed
2. **Caching**: Cache frequently accessed calculations (access requirements, discovery chances)
3. **Batch Processing**: Process multiple nodes together for bulk operations
4. **Memory Management**: Use generators for large path lists, clear unused data

### Scalability Targets

- **Generation Speed**: < 5 seconds for 1000-node labyrinth
- **Access Time**: < 100ms for path access checks
- **Memory Usage**: < 100MB for 10,000-node labyrinth
- **Concurrent Users**: Support 100+ simultaneous users

## Testing Strategy

### Unit Tests

```python
class TestCharacterSystem(unittest.TestCase):
    def test_level_up(self):
        character = CharacterStats()
        character.gain_experience(100)
        self.assertEqual(character.level, 2)
        self.assertEqual(character.courage, 2)
        self.assertEqual(character.perception, 2)

class TestProgressionSystem(unittest.TestCase):
    def test_access_requirements(self):
        character = CharacterStats(level=5, courage=15)
        system = ProgressionSystem(character)
        
        # Create test node
        node = LabyrinthNode(id=1, path="test", depth=3, theme=SemanticAlphabet.HELL)
        can_access, missing = system.check_access(node)
        
        self.assertFalse(can_access)  # Courage requirement not met
        self.assertIn("Courage 10", missing)
```

### Integration Tests

```python
class TestEnhancedLabyrinth(unittest.TestCase):
    def test_rpg_integration(self):
        api = LabyrinthAPI()
        
        # Generate labyrinth
        result = api.generate_labyrinth(50)
        self.assertEqual(len(result['paths']), 50)
        
        # Explore path
        path = result['paths'][0]
        exploration = api.explore_path(path)
        
        self.assertTrue(exploration['exploration_result']['success'])
        self.assertIn('lore', exploration['exploration_result'])
```

## Migration Strategy

### Phase 1: Core Enhancement
1. Extract existing mathematical components
2. Implement RPG mechanics as separate modules
3. Create integration layer
4. Test mathematical preservation

### Phase 2: API Enhancement
1. Enhance existing CLI with RPG features
2. Add character management commands
3. Implement progression tracking
4. Add lore generation options

### Phase 3: Full Integration
1. Replace monolithic script with modular architecture
2. Implement enhanced API
3. Add comprehensive testing
4. Update documentation

This technical specification provides a comprehensive blueprint for enhancing the existing mathematical labyrinth generator with RPG mechanics while preserving its rigorous mathematical foundations and ensuring seamless integration.