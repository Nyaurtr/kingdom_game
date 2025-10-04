"""
Random event system for Kingdom Game Version 3.0
Handles random events with progressive probability and effects
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import random
from .game_config import RANDOM_EVENT_CONFIG, GAME_CONFIG
from .game_state import RandomEvent, RoleResources

@dataclass
class RandomEventTemplate:
    """Template for random events"""
    event_id: str
    name: str
    description: str
    effects: Dict[str, Any]
    event_type: str  # "weather", "social", "economic", "military"

class RandomEventSystem:
    """Manages random events with progressive probability"""
    
    def __init__(self):
        self.config = RANDOM_EVENT_CONFIG
        self.game_config = GAME_CONFIG
        self.event_templates = self._initialize_event_templates()
    
    def _initialize_event_templates(self) -> List[RandomEventTemplate]:
        """Initialize all random event templates"""
        return [
            # Weather Events
            RandomEventTemplate(
                "heavy_rain",
                "Heavy Rain",
                "Heavy rain falls across the kingdom. Visibility is reduced, and military operations are hindered.",
                {"military_effectiveness": -0.2, "investigation_accuracy": -0.1},
                "weather"
            ),
            RandomEventTemplate(
                "drought",
                "Drought",
                "A severe drought affects the kingdom. Food production decreases, and famine vulnerability increases.",
                {"food_production": -0.3, "famine_vulnerability": 0.2},
                "weather"
            ),
            RandomEventTemplate(
                "storm",
                "Storm",
                "A powerful storm sweeps across the kingdom. Trade routes are disrupted, and economic stability is affected.",
                {"trade_disruption": 0.3, "economic_stability": -0.2},
                "weather"
            ),
            RandomEventTemplate(
                "fog",
                "Fog",
                "Thick fog blankets the kingdom. Visibility is reduced, and investigation accuracy is affected.",
                {"investigation_accuracy": -0.3, "military_effectiveness": -0.1},
                "weather"
            ),
            
            # Social Events
            RandomEventTemplate(
                "noble_conflict",
                "Noble Conflict",
                "Noble families are in conflict. Political stability is threatened, and noble support decreases.",
                {"noble_support": -15, "political_stability": -0.2},
                "social"
            ),
            RandomEventTemplate(
                "public_unrest",
                "Public Unrest",
                "Public unrest spreads across the kingdom. Social stability is threatened, and public trust decreases.",
                {"public_trust": -15, "social_stability": -0.2},
                "social"
            ),
            RandomEventTemplate(
                "trade_disruption",
                "Trade Disruption",
                "Trade routes are disrupted by external factors. Economic stability is affected, and resource availability decreases.",
                {"economic_stability": -0.2, "resource_availability": -0.1},
                "social"
            ),
            RandomEventTemplate(
                "religious_tension",
                "Religious Tension",
                "Religious tensions increase across the kingdom. Social cohesion is threatened, and cult vulnerability increases.",
                {"social_cohesion": -0.2, "cult_vulnerability": 0.2},
                "social"
            ),
            
            # Economic Events
            RandomEventTemplate(
                "market_crash",
                "Market Crash",
                "The market experiences a sudden crash. Economic stability is threatened, and treasury resources decrease.",
                {"treasury": -20, "economic_stability": -0.3},
                "economic"
            ),
            RandomEventTemplate(
                "resource_shortage",
                "Resource Shortage",
                "A critical resource shortage affects the kingdom. Resource availability decreases, and preparation becomes more difficult.",
                {"resource_availability": -0.2, "preparation_difficulty": 0.2},
                "economic"
            ),
            RandomEventTemplate(
                "trade_windfall",
                "Trade Windfall",
                "Unexpected trade opportunities arise. Economic stability improves, and treasury resources increase.",
                {"treasury": 20, "economic_stability": 0.2},
                "economic"
            ),
            RandomEventTemplate(
                "resource_discovery",
                "Resource Discovery",
                "New resources are discovered within the kingdom. Resource availability increases, and preparation becomes easier.",
                {"resource_availability": 0.2, "preparation_difficulty": -0.1},
                "economic"
            ),
            
            # Military Events
            RandomEventTemplate(
                "troop_morale_boost",
                "Troop Morale Boost",
                "Your troops experience a morale boost. Military effectiveness improves, and troop loyalty increases.",
                {"troop_loyalty": 15, "military_effectiveness": 0.2},
                "military"
            ),
            RandomEventTemplate(
                "equipment_malfunction",
                "Equipment Malfunction",
                "Equipment malfunctions affect your forces. Military readiness decreases, and soldier count is reduced.",
                {"soldier_count": -10, "military_readiness": -0.2},
                "military"
            ),
            RandomEventTemplate(
                "training_success",
                "Training Success",
                "Your training programs succeed beyond expectations. Military effectiveness improves, and health increases.",
                {"health": 15, "military_effectiveness": 0.2},
                "military"
            ),
            RandomEventTemplate(
                "security_breach",
                "Security Breach",
                "A security breach compromises your operations. Covert effectiveness decreases, and cover identity is reduced.",
                {"cover_identity": -10, "covert_effectiveness": -0.2},
                "military"
            ),
        ]
    
    def should_trigger_random_event(self, day: int) -> bool:
        """Check if random event should trigger based on progressive probability"""
        if day < 1 or day > len(self.config.daily_probability):
            return False
        
        probability = self.config.daily_probability[day - 1]
        return random.random() < probability
    
    def generate_random_event(self, day: int, slot: str) -> Optional[RandomEvent]:
        """Generate a random event for the current day and slot"""
        if not self.should_trigger_random_event(day):
            return None
        
        # Select random event template
        template = random.choice(self.event_templates)
        
        # Create random event
        event = RandomEvent(
            event_id=f"{template.event_id}_{day}_{slot}",
            name=template.name,
            description=template.description,
            day=day,
            slot=slot,
            effects=template.effects.copy(),
            duration=1,
            active=True
        )
        
        return event
    
    def apply_random_event_effects(self, event: RandomEvent, resources: RoleResources, role: str) -> Dict[str, Any]:
        """Apply random event effects to resources"""
        effects_applied = {}
        role_resources = resources.get_resources_for_role(role)
        
        for effect_name, effect_value in event.effects.items():
            if effect_name in role_resources:
                # Direct resource effect
                current_value = role_resources[effect_name]
                if isinstance(effect_value, int):
                    new_value = max(0, min(100, current_value + effect_value))
                    resources.set_resource(role, effect_name, new_value)
                    effects_applied[effect_name] = new_value - current_value
                elif isinstance(effect_value, float):
                    # Percentage effect
                    change = int(current_value * effect_value)
                    new_value = max(0, min(100, current_value + change))
                    resources.set_resource(role, effect_name, new_value)
                    effects_applied[effect_name] = new_value - current_value
            else:
                # Non-resource effect (stored for later use)
                effects_applied[effect_name] = effect_value
        
        return effects_applied
    
    def get_event_probability_for_day(self, day: int) -> float:
        """Get probability of random event for specific day"""
        if day < 1 or day > len(self.config.daily_probability):
            return 0.0
        return self.config.daily_probability[day - 1]
    
    def get_event_description(self, event_id: str) -> str:
        """Get description for specific event"""
        for template in self.event_templates:
            if template.event_id in event_id:
                return template.description
        return "Unknown event"
    
    def get_event_effects_summary(self, event: RandomEvent) -> str:
        """Get summary of event effects"""
        effects_summary = []
        for effect_name, effect_value in event.effects.items():
            if isinstance(effect_value, int):
                if effect_value > 0:
                    effects_summary.append(f"{effect_name} +{effect_value}")
                else:
                    effects_summary.append(f"{effect_name} {effect_value}")
            elif isinstance(effect_value, float):
                percentage = int(effect_value * 100)
                if effect_value > 0:
                    effects_summary.append(f"{effect_name} +{percentage}%")
                else:
                    effects_summary.append(f"{effect_name} {percentage}%")
        
        return ", ".join(effects_summary)
    
    def get_random_event_history_summary(self, events: List[RandomEvent]) -> Dict[str, int]:
        """Get summary of random event history"""
        summary = {}
        for event in events:
            event_type = self._get_event_type(event.event_id)
            summary[event_type] = summary.get(event_type, 0) + 1
        return summary
    
    def _get_event_type(self, event_id: str) -> str:
        """Get event type from event ID"""
        for template in self.event_templates:
            if template.event_id in event_id:
                return template.event_type
        return "unknown"
    
    def get_events_by_type(self, event_type: str) -> List[RandomEventTemplate]:
        """Get all events of specific type"""
        return [template for template in self.event_templates if template.event_type == event_type]
    
    def get_total_events_triggered(self, events: List[RandomEvent]) -> int:
        """Get total number of events triggered"""
        return len(events)
    
    def is_max_events_reached(self, events: List[RandomEvent]) -> bool:
        """Check if maximum events per game reached"""
        return len(events) >= self.config.max_events_per_game
    
    def is_min_events_met(self, events: List[RandomEvent]) -> bool:
        """Check if minimum events per game met"""
        return len(events) >= self.config.min_events_per_game
