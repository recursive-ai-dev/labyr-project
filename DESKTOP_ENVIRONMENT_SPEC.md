# Diegetic Desktop Environment Implementation Specification

## Overview

This document specifies the implementation of the diegetic desktop environment that transforms the user's computer interface into an immersive dark fantasy world. This layer sits above the enhanced labyrinth engine and provides the visual, auditory, and interactive elements that make the filesystem feel like a living fantasy realm.

## Core Design Principles

### 1. Complete Diegetic Integration
- **No non-diegetic overlays** - every UI element exists within the fantasy world
- **Environmental storytelling** - the desktop background tells a story
- **Contextual interactions** - cursor and actions change based on location
- **Atmospheric consistency** - all elements maintain dark fantasy tone

### 2. Performance & Compatibility
- **60fps operation** on mid-range hardware
- **Cross-platform support** (Windows, macOS, Linux)
- **Seamless integration** with existing desktop environments
- **Resource efficiency** - minimal impact on system performance

### 3. User Experience
- **Intuitive navigation** - familiar file operations with fantasy presentation
- **Progressive discovery** - users uncover the world gradually
- **Accessibility** - support for various user needs
- **Customization** - multiple fantasy themes and intensity levels

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    DIEGETIC DESKTOP LAYER                   │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              ENVIRONMENT RENDERER                       │ │
│  │  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Desktop         │  │ Weather &       │              │ │
│  │  │ Background      │  │ Lighting        │              │ │
│  │  │ System          │  │ Effects         │              │ │
│  │  └─────────────────┘  └─────────────────┘              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Particle        │  │ Animation       │              │ │
│  │  │ System          │  │ Controller      │              │ │
│  │  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                INTERACTION LAYER                        │ │
│  │  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Diegetic        │  │ Contextual      │              │ │
│  │  │ Cursor System   │  │ Notifications   │              │ │
│  │  └─────────────────┘  └─────────────────┘              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Hover Effects   │  │ Click Animations│              │ │
│  │  │ & Feedback      │  │ & Transitions   │              │ │
│  │  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 AUDIO SYSTEM                            │ │
│  │  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Ambient         │  │ Interactive     │              │ │
│  │  │ Soundscapes     │  │ Audio Feedback  │              │ │
│  │  └─────────────────┘  └─────────────────┘              │ │
│  │  ┌─────────────────┐  ┌─────────────────┐              │ │
│  │  │ Dynamic         │  │ Spatial         │              │ │
│  │  │ Volume Control  │  │ Audio Positioning│              │ │
│  │  └─────────────────┘  └─────────────────┘              │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Component Specifications

### 1. Environment Renderer (`environment.py`)

```python
class EnvironmentRenderer:
    """Manages the diegetic desktop background and environmental effects."""
    
    def __init__(self):
        self.current_theme = "gothic_cityscape"
        self.weather_system = WeatherSystem()
        self.lighting_system = LightingSystem()
        self.particle_system = ParticleSystem()
        self.animation_controller = AnimationController()
        
    def set_theme(self, theme_name: str):
        """Change the overall theme of the environment."""
        themes = {
            "gothic_cityscape": GothicCityscapeTheme(),
            "candlelit_library": CandlelitLibraryTheme(),
            "storm_wrecked": StormWreckedTheme(),
            "forbidden_library": ForbiddenLibraryTheme()
        }
        
        if theme_name in themes:
            self.current_theme = theme_name
            self.apply_theme(themes[theme_name])
            
    def apply_theme(self, theme: Theme):
        """Apply a theme's visual and audio properties."""
        # Update desktop background
        self.update_background(theme.background_config)
        
        # Update color palette
        self.update_color_scheme(theme.color_scheme)
        
        # Update ambient sounds
        self.update_ambient_audio(theme.ambient_sounds)
        
        # Update particle effects
        self.update_particle_effects(theme.particle_config)
        
    def update_background(self, config: Dict):
        """Update the desktop background with animated elements."""
        if config['type'] == 'animated':
            self.animated_background = AnimatedBackground(config)
        elif config['type'] == 'static':
            self.static_background = StaticBackground(config)
            
    def render_frame(self):
        """Render a single frame of the environment."""
        # Update weather effects
        weather_effects = self.weather_system.get_current_effects()
        
        # Update lighting based on time and weather
        lighting = self.lighting_system.calculate_lighting(weather_effects)
        
        # Update particle system
        particles = self.particle_system.update()
        
        # Render background with effects
        frame = self.render_background_with_effects(weather_effects, lighting, particles)
        
        # Apply post-processing effects
        frame = self.apply_post_processing(frame, lighting)
        
        return frame
```

### 2. Theme System (`themes.py`)

```python
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
                'primary': '#2a1a3d',    # Deep purple
                'secondary': '#8b0000',  # Dark red
                'accent': '#ffd700',     # Gold
                'text': '#ffffff',       # White
                'shadow': '#000000'      # Black
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

class CandlelitLibraryTheme(Theme):
    """Candlelit library interior with flickering effects."""
    
    def __init__(self):
        super().__init__(
            name="candlelit_library",
            background_config={
                'type': 'animated',
                'base_image': 'assets/themes/candlelit_library/base.jpg',
                'animations': [
                    {'layer': 'candles', 'animation': 'flicker', 'speed': 1.5},
                    {'layer': 'shadows', 'animation': 'dance', 'speed': 0.5},
                    {'layer': 'dust', 'animation': 'float', 'speed': 0.1}
                ]
            },
            color_scheme={
                'primary': '#1a1a1a',    # Dark gray
                'secondary': '#8b4513',  # Brown
                'accent': '#ffd700',     # Candlelight gold
                'text': '#f5deb3',       # Beige
                'shadow': '#000000'      # Black
            },
            ambient_sounds=[
                'crackling_fire.wav',
                'page_turning.wav',
                'distant_whispers.wav',
                'clock_ticking.wav'
            ],
            particle_config={
                'dust': {'density': 0.6, 'speed': 0.05, 'size': 1},
                'embers': {'density': 0.2, 'speed': 0.2, 'size': 2},
                'magic_sparks': {'density': 0.1, 'speed': 0.8, 'size': 1}
            },
            cursor_styles={
                'default': 'quill_pen',
                'hover': 'magnifying_glass',
                'click': 'ink_splash'
            },
            notification_styles={
                'scroll': 'ancient_tome',
                'whisper': 'library_echo',
                'rune': 'arcane_symbol'
            }
        )
```

### 3. Diegetic Cursor System (`cursor.py`)

```python
class DiegeticCursor:
    """Manages the fantasy-themed cursor system."""
    
    def __init__(self, renderer: EnvironmentRenderer):
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
            return self.renderer.current_theme.cursor_styles['default']
            
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
            return self.renderer.current_theme.cursor_styles['hover']
            
    def render(self, surface):
        """Render the cursor at current position."""
        cursor_config = self.get_cursor_config()
        
        # Apply hover effects
        if self.hover_state:
            cursor_config = self.apply_hover_effects(cursor_config)
            
        # Render cursor animation
        self.render_cursor_animation(surface, cursor_config)
        
    def get_cursor_config(self) -> Dict:
        """Get configuration for current cursor style."""
        styles = {
            'spectral_hand': {
                'image': 'assets/cursors/spectral_hand.png',
                'animation_frames': 8,
                'glow_radius': 10,
                'trail_length': 5
            },
            'magnifying_glass': {
                'image': 'assets/cursors/magnifying_glass.png',
                'animation_frames': 4,
                'magnification': 1.5,
                'glow_radius': 5
            },
            'glowing_orb': {
                'image': 'assets/cursors/glowing_orb.png',
                'animation_frames': 12,
                'pulse_speed': 0.1,
                'color_shift': True
            },
            'shadow_tendril': {
                'image': 'assets/cursors/shadow_tendril.png',
                'animation_frames': 6,
                'opacity_pulse': True,
                'fear_effect': True
            }
        }
        
        return styles.get(self.current_style, styles['spectral_hand'])
        
    def apply_hover_effects(self, config: Dict) -> Dict:
        """Apply hover-specific effects to cursor configuration."""
        if self.hover_state == 'interactive':
            config['glow_radius'] = config.get('glow_radius', 0) * 1.5
            config['animation_speed'] = config.get('animation_speed', 1.0) * 2.0
        elif self.hover_state == 'dangerous':
            config['color'] = (255, 0, 0)  # Red warning color
            config['shake_intensity'] = 2
        elif self.hover_state == 'magical':
            config['sparkle_density'] = 0.8
            config['arcane_symbols'] = True
            
        return config
```

### 4. Contextual Notification System (`notifications.py`)

```python
class ContextualNotification:
    """Manages fantasy-themed notifications and feedback."""
    
    def __init__(self, renderer: EnvironmentRenderer):
        self.renderer = renderer
        self.active_notifications: List[Notification] = []
        
    def show_notification(self, message: str, notification_type: str = "scroll"):
        """Show a contextual notification."""
        notification = Notification(
            message=message,
            type=notification_type,
            theme=self.renderer.current_theme,
            position=self.calculate_position()
        )
        
        self.active_notifications.append(notification)
        
    def calculate_position(self) -> Tuple[int, int]:
        """Calculate optimal position for notification."""
        # Position near cursor but not obstructing
        cursor_x, cursor_y = pygame.mouse.get_pos()
        
        # Avoid screen edges
        x = max(50, min(cursor_x - 100, 1800))
        y = max(50, min(cursor_y - 50, 1000))
        
        return (x, y)
        
    def render_notifications(self, surface):
        """Render all active notifications."""
        for notification in self.active_notifications[:]:
            if notification.is_expired():
                self.active_notifications.remove(notification)
            else:
                self.render_notification(surface, notification)
                
    def render_notification(self, surface, notification: Notification):
        """Render a single notification with appropriate style."""
        if notification.type == "scroll":
            self.render_scroll_notification(surface, notification)
        elif notification.type == "whisper":
            self.render_whisper_notification(surface, notification)
        elif notification.type == "rune":
            self.render_rune_notification(surface, notification)
            
    def render_scroll_notification(self, surface, notification: Notification):
        """Render notification as an unfurling scroll."""
        # Draw scroll background
        scroll_rect = pygame.Rect(notification.position[0], notification.position[1], 300, 100)
        pygame.draw.rect(surface, (210, 180, 140), scroll_rect, border_radius=10)  # Beige scroll
        pygame.draw.rect(surface, (139, 69, 19), scroll_rect, 3, border_radius=10)  # Brown border
        
        # Draw scroll texture
        self.draw_scroll_texture(surface, scroll_rect)
        
        # Draw message text
        font = pygame.font.Font('assets/fonts/ancient.ttf', 16)
        text_surface = font.render(notification.message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=scroll_rect.center)
        surface.blit(text_surface, text_rect)
        
        # Draw scroll ends
        pygame.draw.ellipse(surface, (139, 69, 19), (scroll_rect.left - 10, scroll_rect.top - 5, 20, 110))
        pygame.draw.ellipse(surface, (139, 69, 19), (scroll_rect.right - 10, scroll_rect.top - 5, 20, 110))
        
    def render_whisper_notification(self, surface, notification: Notification):
        """Render notification as ghostly whisper text."""
        # Create ghostly text effect
        font = pygame.font.Font('assets/fonts/ghostly.ttf', 20)
        text_surface = font.render(notification.message, True, (255, 255, 255))
        
        # Apply transparency and glow
        text_surface.set_alpha(128)
        
        # Add floating animation
        float_offset = math.sin(pygame.time.get_ticks() * 0.005) * 5
        position = (notification.position[0], notification.position[1] + float_offset)
        
        surface.blit(text_surface, position)
        
    def draw_scroll_texture(self, surface, rect):
        """Draw parchment texture on scroll."""
        # Create subtle noise pattern for parchment effect
        for _ in range(50):
            x = random.randint(rect.left, rect.right)
            y = random.randint(rect.top, rect.bottom)
            size = random.randint(1, 2)
            alpha = random.randint(100, 150)
            pygame.draw.circle(surface, (0, 0, 0, alpha), (x, y), size)
```

### 5. Audio System (`audio.py`)

```python
class AudioSystem:
    """Manages atmospheric and interactive audio."""
    
    def __init__(self):
        self.ambient_player = AmbientPlayer()
        self.interactive_player = InteractivePlayer()
        self.spatial_engine = SpatialAudioEngine()
        self.volume_controller = VolumeController()
        
    def set_theme(self, theme: Theme):
        """Set audio theme based on environment."""
        self.ambient_player.load_sounds(theme.ambient_sounds)
        self.ambient_player.start_ambient_loop()
        
    def play_interaction_sound(self, interaction_type: str, position: Tuple[int, int]):
        """Play sound for specific interaction."""
        sounds = {
            'click': 'magic_click.wav',
            'hover': 'mystical_hum.wav',
            'open': 'ancient_door.wav',
            'discover': 'triumphant_chime.wav',
            'error': 'ominous_drum.wav'
        }
        
        if interaction_type in sounds:
            self.interactive_player.play_sound(
                sounds[interaction_type],
                position=position,
                volume=self.volume_controller.get_interaction_volume()
            )
            
    def play_discovery_sound(self, discovery_type: str):
        """Play sound for discoveries."""
        discovery_sounds = {
            'hidden_chamber': 'secret_revealed.wav',
            'ancient_tome': 'wisdom_gained.wav',
            'forbidden_knowledge': 'cosmic_horror.wav',
            'rare_artifact': 'treasure_found.wav'
        }
        
        sound = discovery_sounds.get(discovery_type, 'discovery_generic.wav')
        self.interactive_player.play_sound(sound, volume=0.8)
        
    def update_ambient_volume(self, weather_intensity: float):
        """Adjust ambient volume based on weather."""
        base_volume = self.volume_controller.get_ambient_volume()
        weather_modifier = 1.0 + (weather_intensity * 0.5)  # Louder during storms
        
        self.ambient_player.set_volume(base_volume * weather_modifier)
```

### 6. Weather & Lighting System (`weather.py`)

```python
class WeatherSystem:
    """Manages dynamic weather effects."""
    
    def __init__(self):
        self.current_weather = "clear"
        self.weather_intensity = 0.0
        self.weather_timer = 0
        
    def update(self):
        """Update weather conditions."""
        self.weather_timer += 1
        
        # Random weather changes every 30-60 seconds
        if self.weather_timer > random.randint(1800, 3600):
            self.change_weather()
            self.weather_timer = 0
            
        # Update intensity for current weather
        if self.current_weather != "clear":
            self.weather_intensity = min(1.0, self.weather_intensity + 0.01)
        else:
            self.weather_intensity = max(0.0, self.weather_intensity - 0.02)
            
    def change_weather(self):
        """Change to a new weather condition."""
        weather_types = ["clear", "cloudy", "rain", "storm", "fog", "snow"]
        
        # Don't repeat the same weather
        new_weather = random.choice([w for w in weather_types if w != self.current_weather])
        
        self.current_weather = new_weather
        self.weather_intensity = 0.1
        
        # Notify audio system
        if hasattr(self, 'audio_system'):
            self.audio_system.play_weather_change_sound(new_weather)
            
    def get_current_effects(self) -> Dict:
        """Get current weather effects."""
        return {
            'type': self.current_weather,
            'intensity': self.weather_intensity,
            'lighting_modifier': self.get_lighting_modifier(),
            'particle_density': self.get_particle_density()
        }
        
    def get_lighting_modifier(self) -> float:
        """Get lighting modifier for current weather."""
        modifiers = {
            "clear": 1.0,
            "cloudy": 0.8,
            "rain": 0.6,
            "storm": 0.3,
            "fog": 0.5,
            "snow": 0.7
        }
        return modifiers.get(self.current_weather, 1.0) * (1.0 - self.weather_intensity * 0.5)
        
    def get_particle_density(self) -> float:
        """Get particle density for current weather."""
        densities = {
            "clear": 0.0,
            "cloudy": 0.1,
            "rain": 0.8,
            "storm": 1.0,
            "fog": 0.6,
            "snow": 0.4
        }
        return densities.get(self.current_weather, 0.0) * self.weather_intensity
```

## Implementation Strategy

### Phase 1: Core Environment System (Week 1)
1. **Environment Renderer**: Basic background rendering with theme switching
2. **Theme System**: Gothic cityscape and candlelit library themes
3. **Audio System**: Ambient soundscapes and basic interaction sounds
4. **Weather System**: Dynamic weather with visual and audio effects

### Phase 2: Interaction Layer (Week 2)
1. **Diegetic Cursor**: Fantasy-themed cursor with contextual styles
2. **Notification System**: Scroll, whisper, and rune notification styles
3. **Hover Effects**: Contextual feedback for different file types
4. **Click Animations**: Thematic animations for file operations

### Phase 3: Polish & Optimization (Week 3)
1. **Performance Optimization**: 60fps target with efficient rendering
2. **Cross-Platform Support**: Windows, macOS, Linux compatibility
3. **Accessibility Features**: Colorblind modes, keyboard navigation
4. **Customization Options**: Theme intensity, performance settings

## Technical Requirements

### Core Technologies
- **Python** with **Pygame** for rendering and input handling
- **OpenAL** or **pygame.mixer** for 3D audio positioning
- **OpenGL** via **PyOpenGL** for advanced visual effects
- **Platform-specific APIs** for desktop integration

### Performance Targets
- **60fps** operation on mid-range hardware (GTX 1060 equivalent)
- **<100MB** memory usage for environment layer
- **<5%** CPU usage when idle
- **<10ms** input response time

### Compatibility Requirements
- **Windows 10+**, **macOS 10.14+**, **Linux** (Ubuntu 18.04+)
- **Multiple desktop environments**: GNOME, KDE, Windows Explorer, macOS Finder
- **Resolution support**: 1080p to 4K displays
- **DPI scaling**: High DPI display support

## Integration with Labyrinth Engine

### Data Flow
```
Labyrinth Engine → Environment Renderer → Desktop Display
     ↓                    ↓                    ↓
Character Stats → Theme Selection → Visual Effects
Progression → Weather Intensity → Audio Changes
Discovery → Notification Type → User Feedback
```

### API Integration
```python
class DesktopEnvironment:
    """Main interface for diegetic desktop environment."""
    
    def __init__(self, labyrinth_api: LabyrinthAPI):
        self.labyrinth_api = labyrinth_api
        self.renderer = EnvironmentRenderer()
        self.cursor = DiegeticCursor(self.renderer)
        self.notifications = ContextualNotification(self.renderer)
        self.audio = AudioSystem()
        
    def update(self):
        """Update environment based on labyrinth state."""
        # Get character status
        status = self.labyrinth_api.get_character_status()
        
        # Update theme based on character progression
        self.update_theme_for_progression(status)
        
        # Update weather based on exploration
        self.update_weather_for_exploration(status)
        
        # Update audio based on current area
        self.update_audio_for_location(status)
        
    def handle_file_operation(self, operation: str, file_path: str):
        """Handle file operations with diegetic feedback."""
        # Determine appropriate cursor and notification
        self.cursor.update_style_for_operation(operation, file_path)
        
        # Play appropriate sound
        self.audio.play_interaction_sound(operation, self.cursor.position)
        
        # Show contextual notification
        message = self.generate_operation_message(operation, file_path)
        self.notifications.show_notification(message, self.get_notification_type(operation))
```

This specification provides a comprehensive blueprint for implementing the diegetic desktop environment that transforms the mathematical labyrinth into an immersive dark fantasy experience while maintaining performance and compatibility requirements.