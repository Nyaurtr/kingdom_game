# Kingdom Game Version 3.0 - Narrative Investigation Game

A medieval fantasy investigation game where you play as one of three roles (King, Captain, or Spy) to solve a kingdom crisis within 7 days. This version implements the complete GDD 3.0 with resource management, preparation actions, and evidence pools.

## Features Implemented

### ✅ Core Systems (GDD 3.0)
- **Random Role Assignment**: Each game randomly assigns King/Captain/Spy with unique personal secrets
- **Resource Management**: Role-specific resources with transfer costs and acquisition actions
- **Preparation System**: Crisis-specific preparation actions with effectiveness scaling
- **Investigation System**: Priority-based evidence pools (Low/Medium/High) with role-specific methods
- **Random Events**: Background events with progressive probability and resource effects
- **Content System**: Comprehensive dialogues, narratives, and ending messages

### ✅ 8 Crisis Events
1. **Famine Cascade**: Food shortage crisis affecting kingdom stability
2. **Pandemic Surge**: Disease outbreak threatening population health
3. **Invasion/Rebellion**: Military threat from internal or external forces
4. **Cult Uprising**: Supernatural/religious threat disrupting social order
5. **Environmental Catastrophe**: Natural disasters threatening the kingdom
6. **Crop Blight**: Agricultural crisis affecting food production
7. **Economic Collapse**: Financial crisis threatening kingdom stability
8. **Supernatural Rift**: Otherworldly threat disrupting reality

### ✅ GUI System (7-Section Layout)
- **Resources Section**: Display current resource values with transfer options
- **Actions Section**: Resource acquisition and preparation actions
- **Investigation Section**: Investigation methods and evidence count
- **Preparation Progress Section**: Effectiveness tracking and status
- **Time Section**: Day/slot progression with advance button
- **Main Screen Section**: Narrative content and action results
- **Role Character Section**: Role description and personal secret status

### ✅ Game Mechanics
- **7-Day Timeline**: Morning/Afternoon/Evening progression (21 total action slots)
- **Resource Transfer**: Convert resources with 10% cost (configurable)
- **Preparation Effectiveness**: 3 levels (Low/Medium/High) affecting crisis resolution
- **Evidence Pools**: 20+ Low priority, 15+ Medium priority, 10+ High priority per event
- **Random Events**: 3-5 events per game with progressive probability
- **Crisis Resolution**: Based on preparation effectiveness (0.6+ partial recovery, 0.9+ kingdom saved)

## How to Play

1. **Start Game**: Run `python main.py`
2. **Role Assignment**: Game randomly assigns your role (King/Captain/Spy)
3. **Investigate**: Use investigation methods to gather evidence from priority pools
4. **Acquire Resources**: Use resource acquisition actions to gain resources
5. **Prepare**: Use preparation actions to mitigate the coming crisis
6. **Advance Time**: Progress through 7 days (21 action slots total)
7. **Crisis Resolution**: Game determines ending based on preparation effectiveness

## Technical Implementation

### Architecture
- **MVC Pattern**: Model (game state), View (GUI), Controller (game logic)
- **Component System**: Modular systems for roles, resources, preparation, investigation
- **Event-Driven**: GUI responds to game state changes
- **JSON Data**: Evidence pools stored in separate JSON files for easy modification

### File Structure
```
kingdom_game/
├── src/
│   ├── core/                    # Core game systems
│   │   ├── game_state.py       # Main game state and data structures
│   │   ├── role_system.py      # Role definitions and actions
│   │   ├── resource_system.py  # Resource management and transfers
│   │   ├── preparation_system.py # Preparation actions and effectiveness
│   │   ├── investigation.py    # Investigation methods and evidence pools
│   │   ├── random_event_system.py # Random events and effects
│   │   ├── content_system.py   # Dialogues, narratives, and endings
│   │   ├── game_config.py      # Game constants and configuration
│   │   └── evidence_pools/     # JSON files with evidence for each event
│   ├── ui/                     # GUI system
│   │   └── gui.py             # 7-section layout GUI
│   └── main.py                # Main game controller
├── tests/                      # Test files
└── main.py                    # Entry point
```

## Testing

The game has been thoroughly tested with:
- **Core Mechanics**: All systems tested with different roles and events
- **Resource Balance**: All actions are affordable with starting resources
- **Effectiveness Scaling**: Clear thresholds for crisis resolution
- **GUI Integration**: 7-section layout working correctly
- **Content Integration**: All dialogues and narratives implemented

## Game Design Document

This implementation is based on the comprehensive GDD version 3.0, which includes:
- **Resource Management**: Role-specific resources with transfer costs
- **Preparation System**: Crisis-specific actions with effectiveness scaling
- **Evidence Pools**: Priority-based evidence with role-specific access
- **Random Events**: Background events with progressive probability
- **Content System**: Comprehensive dialogues and narratives

The game successfully implements the narrative-first investigation mechanics with resource management and preparation actions, creating a strategic yet story-driven experience.
