"""
Core game state management
Contains the main GameState class that tracks all game data
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json
from datetime import datetime
from .game_config import GAME_CONFIG

class MeterState(Enum):
    """States for the 4 main kingdom meters"""
    STABLE = "stable"
    STRAINED = "strained" 
    CRITICAL = "critical"

class TrustLevel(Enum):
    """Trust levels for NPCs and sources"""
    SUSPICIOUS = "suspicious"
    NEUTRAL = "neutral"
    TRUSTED = "trusted"
    LOYAL = "loyal"
    DEVOTED = "devoted"

class GamePhase(Enum):
    """Current phase of the game story"""
    ACT_I = "act_i"      # Days 1-2: Setup
    ACT_II = "act_ii"    # Days 3-4: Rising Action  
    ACT_III = "act_iii"  # Days 5-6: Crisis
    EPILOGUE = "epilogue" # Day 7: Resolution

@dataclass
class RoleResources:
    """Resource system for each role"""
    # King resources
    treasury: int = GAME_CONFIG.initial_resource_value
    food_reserves: int = GAME_CONFIG.initial_resource_value
    public_trust: int = GAME_CONFIG.initial_resource_value
    noble_support: int = GAME_CONFIG.initial_resource_value
    
    # Captain resources
    personal_funds: int = GAME_CONFIG.initial_resource_value
    health: int = GAME_CONFIG.initial_resource_value
    troop_loyalty: int = GAME_CONFIG.initial_resource_value
    soldier_count: int = GAME_CONFIG.initial_resource_value
    
    # Spy resources
    cover_identity: int = GAME_CONFIG.initial_resource_value
    network_contacts: int = GAME_CONFIG.initial_resource_value
    covert_funds: int = GAME_CONFIG.initial_resource_value
    intelligence: int = GAME_CONFIG.initial_resource_value
    
    def get_resources_for_role(self, role: str) -> Dict[str, int]:
        """Get resources for specific role"""
        if role == "king":
            return {
                "treasury": self.treasury,
                "food_reserves": self.food_reserves,
                "public_trust": self.public_trust,
                "noble_support": self.noble_support
            }
        elif role == "captain":
            return {
                "personal_funds": self.personal_funds,
                "health": self.health,
                "troop_loyalty": self.troop_loyalty,
                "soldier_count": self.soldier_count
            }
        elif role == "spy":
            return {
                "cover_identity": self.cover_identity,
                "network_contacts": self.network_contacts,
                "covert_funds": self.covert_funds,
                "intelligence": self.intelligence
            }
        return {}
    
    def set_resource(self, role: str, resource_name: str, value: int) -> None:
        """Set resource value for specific role"""
        value = max(GAME_CONFIG.min_resource_value, min(GAME_CONFIG.max_resource_value, value))
        
        if role == "king":
            if resource_name == "treasury":
                self.treasury = value
            elif resource_name == "food_reserves":
                self.food_reserves = value
            elif resource_name == "public_trust":
                self.public_trust = value
            elif resource_name == "noble_support":
                self.noble_support = value
        elif role == "captain":
            if resource_name == "personal_funds":
                self.personal_funds = value
            elif resource_name == "health":
                self.health = value
            elif resource_name == "troop_loyalty":
                self.troop_loyalty = value
            elif resource_name == "soldier_count":
                self.soldier_count = value
        elif role == "spy":
            if resource_name == "cover_identity":
                self.cover_identity = value
            elif resource_name == "network_contacts":
                self.network_contacts = value
            elif resource_name == "covert_funds":
                self.covert_funds = value
            elif resource_name == "intelligence":
                self.intelligence = value

@dataclass
class PreparationProgress:
    """Track preparation progress for each event"""
    event_id: str
    preparation_actions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    total_effectiveness: float = 0.0
    preparation_complete: bool = False
    
    def add_preparation_action(self, action_id: str, resource_cost: Dict[str, int], effectiveness: float) -> None:
        """Add a preparation action"""
        self.preparation_actions[action_id] = {
            "resource_cost": resource_cost,
            "effectiveness": effectiveness,
            "completed": True
        }
        self.total_effectiveness += effectiveness
    
    def get_total_effectiveness(self) -> float:
        """Get total preparation effectiveness"""
        return min(1.0, self.total_effectiveness)  # Cap at 100%

@dataclass
class RandomEvent:
    """Random event that affects the kingdom"""
    event_id: str
    name: str
    description: str
    day: int
    slot: str
    effects: Dict[str, Any] = field(default_factory=dict)
    duration: int = 1  # Number of slots
    active: bool = True

@dataclass
class NPC:
    """Non-player character with relationship tracking"""
    id: str
    name: str
    role_relevance: str  # "all", "king", "captain", "spy"
    trust_level: TrustLevel = TrustLevel.NEUTRAL
    hidden_agenda: Optional[str] = None
    secret_status: Optional[str] = None
    relationship_arc: str = "neutral"
    resources: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)

@dataclass
class Evidence:
    """Investigation evidence/clue"""
    id: str
    content: str
    reliability: str  # "low", "medium", "high"
    source_type: str  # "rumor", "official", "physical", "laboratory", "intercepted", "market", "prophetic"
    source_id: str
    discovered_day: int
    location: str
    verified: bool = False

@dataclass
class PersonalSecret:
    """Player character's personal secret"""
    secret_id: str
    revealed: bool = False
    impact_level: float = 0.0
    resolution_status: str = "hidden"  # "hidden", "confessed", "resolved", "exploited"

@dataclass
class GameState:
    """Main game state container"""
    # Core game info
    current_role: str = ""  # "king", "captain", "spy"
    current_day: int = 1
    current_slot: str = "morning"  # "morning", "afternoon", "evening"
    game_phase: GamePhase = GamePhase.ACT_I
    
    # Resource system (NEW)
    resources: RoleResources = field(default_factory=RoleResources)
    
    # Preparation system (NEW)
    preparation_progress: Dict[str, PreparationProgress] = field(default_factory=dict)
    
    # Random events (NEW)
    active_random_events: List[RandomEvent] = field(default_factory=list)
    random_event_history: List[RandomEvent] = field(default_factory=list)
    
    # Character state
    personal_secret: Optional[PersonalSecret] = None
    signature_action_used: bool = False
    
    # NPCs and relationships
    npcs: Dict[str, NPC] = field(default_factory=dict)
    
    # Investigation state
    evidence: List[Evidence] = field(default_factory=list)
    investigation_focus: str = ""
    caseboard_connections: Dict[str, List[str]] = field(default_factory=dict)
    
    # Story state
    primary_event: Optional[str] = None
    secondary_event: Optional[str] = None
    background_incidents: List[str] = field(default_factory=list)
    
    # Omen system (DEPRECATED - will be removed)
    received_omens: List[str] = field(default_factory=list)
    
    # Story flags
    story_flags: Dict[str, Any] = field(default_factory=dict)
    
    # Ending preparation
    ending_category: Optional[str] = None
    ending_variation: Optional[str] = None
    
    # Action tracking (NEW)
    actions_taken: List[Dict[str, Any]] = field(default_factory=list)
    current_action_category: Optional[str] = None  # "investigation", "resource", "preparation"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "current_role": self.current_role,
            "current_day": self.current_day,
            "current_slot": self.current_slot,
            "game_phase": self.game_phase.value,
            "meters": {
                "food_supply": self.meters.food_supply.value,
                "disease_pressure": self.meters.disease_pressure.value,
                "public_order": self.meters.public_order.value,
                "treasury": self.meters.treasury.value
            },
            "personal_secret": {
                "secret_id": self.personal_secret.secret_id if self.personal_secret else None,
                "revealed": self.personal_secret.revealed if self.personal_secret else False,
                "impact_level": self.personal_secret.impact_level if self.personal_secret else 0.0,
                "resolution_status": self.personal_secret.resolution_status if self.personal_secret else "hidden"
            } if self.personal_secret else None,
            "signature_action_used": self.signature_action_used,
            "npcs": {npc_id: {
                "id": npc.id,
                "name": npc.name,
                "role_relevance": npc.role_relevance,
                "trust_level": npc.trust_level.value,
                "hidden_agenda": npc.hidden_agenda,
                "secret_status": npc.secret_status,
                "relationship_arc": npc.relationship_arc,
                "resources": npc.resources,
                "conflicts": npc.conflicts
            } for npc_id, npc in self.npcs.items()},
            "evidence": [{
                "id": ev.id,
                "content": ev.content,
                "reliability": ev.reliability,
                "source_type": ev.source_type,
                "source_id": ev.source_id,
                "discovered_day": ev.discovered_day,
                "location": ev.location,
                "verified": ev.verified
            } for ev in self.evidence],
            "investigation_focus": self.investigation_focus,
            "caseboard_connections": self.caseboard_connections,
            "primary_event": self.primary_event,
            "secondary_event": self.secondary_event,
            "background_incidents": self.background_incidents,
            "received_omens": self.received_omens,
            "story_flags": self.story_flags,
            "ending_category": self.ending_category,
            "ending_variation": self.ending_variation
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameState':
        """Create GameState from dictionary"""
        game_state = cls()
        game_state.current_role = data.get("current_role", "")
        game_state.current_day = data.get("current_day", 1)
        game_state.current_slot = data.get("current_slot", "morning")
        game_state.game_phase = GamePhase(data.get("game_phase", "act_i"))
        
        # Meters
        meters_data = data.get("meters", {})
        game_state.meters = KingdomMeters(
            food_supply=MeterState(meters_data.get("food_supply", "stable")),
            disease_pressure=MeterState(meters_data.get("disease_pressure", "stable")),
            public_order=MeterState(meters_data.get("public_order", "stable")),
            treasury=MeterState(meters_data.get("treasury", "stable"))
        )
        
        # Personal secret
        secret_data = data.get("personal_secret")
        if secret_data:
            game_state.personal_secret = PersonalSecret(
                secret_id=secret_data.get("secret_id", ""),
                revealed=secret_data.get("revealed", False),
                impact_level=secret_data.get("impact_level", 0.0),
                resolution_status=secret_data.get("resolution_status", "hidden")
            )
        
        game_state.signature_action_used = data.get("signature_action_used", False)
        
        # NPCs
        npcs_data = data.get("npcs", {})
        for npc_id, npc_data in npcs_data.items():
            game_state.npcs[npc_id] = NPC(
                id=npc_data["id"],
                name=npc_data["name"],
                role_relevance=npc_data["role_relevance"],
                trust_level=TrustLevel(npc_data["trust_level"]),
                hidden_agenda=npc_data.get("hidden_agenda"),
                secret_status=npc_data.get("secret_status"),
                relationship_arc=npc_data.get("relationship_arc", "neutral"),
                resources=npc_data.get("resources", []),
                conflicts=npc_data.get("conflicts", [])
            )
        
        # Evidence
        evidence_data = data.get("evidence", [])
        for ev_data in evidence_data:
            game_state.evidence.append(Evidence(
                id=ev_data["id"],
                content=ev_data["content"],
                reliability=ev_data["reliability"],
                source_type=ev_data["source_type"],
                source_id=ev_data["source_id"],
                discovered_day=ev_data["discovered_day"],
                location=ev_data["location"],
                verified=ev_data.get("verified", False)
            ))
        
        game_state.investigation_focus = data.get("investigation_focus", "")
        game_state.caseboard_connections = data.get("caseboard_connections", {})
        game_state.primary_event = data.get("primary_event")
        game_state.secondary_event = data.get("secondary_event")
        game_state.background_incidents = data.get("background_incidents", [])
        game_state.received_omens = data.get("received_omens", [])
        game_state.story_flags = data.get("story_flags", {})
        game_state.ending_category = data.get("ending_category")
        game_state.ending_variation = data.get("ending_variation")
        
        return game_state
